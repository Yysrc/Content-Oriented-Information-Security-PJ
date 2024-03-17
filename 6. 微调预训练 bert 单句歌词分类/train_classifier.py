import os
from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
from datasets import Dataset


def load_data(trainsdir):
    documents = []
    labels = []
    subdirs = os.walk(trainsdir)
    for d, _, fns in subdirs:
        for fn in fns:
            if fn[-3:] == 'txt':
                filepath = os.path.join(d, fn)
                f = open(filepath, "r", encoding="utf-8")
                file_content = f.readlines()
                filtered_content = [
                    line[:-1] for line in file_content if ':' not in line and '：' not in line]
                documents += filtered_content
                labels += [d[d.rindex(os.sep)+1:]] * len(filtered_content)
    return documents, labels


if __name__ == "__main__":
    singers = ["陈奕迅", "刀郎", "周杰伦", "孙燕姿", "小虎队",
               "崔健", "王菲", "罗大佑", "薛之谦", "许嵩", "邓丽君", "邓紫棋"]

    id2label = {idx: label for idx, label in enumerate(singers)}
    label2id = {label: idx for idx, label in enumerate(singers)}

    train_dicts = ["./music/a song in a text/" + name for name in singers]
    docs, labels = [], []
    for dic in train_dicts:
        doc, label = load_data(dic)
        docs += doc
        labels += label

    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-chinese", 
        num_labels=len(singers), 
        id2label=id2label, 
        label2id=label2id
    )

    tokenized_docs = tokenizer(
        docs, padding=True, truncation=True, max_length=512)
    
    labels = [label2id[l] for l in labels]

    dataset = Dataset.from_dict(
        {'input_ids': tokenized_docs['input_ids'], 
         'attention_mask': tokenized_docs['attention_mask'], 
         'labels': labels,
         })
    
    train_dataset, test_dataset = dataset.train_test_split(test_size=0.1).values()

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs', 
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )

    print("Training starts\n")
    trainer.train()
    trainer.evaluate()