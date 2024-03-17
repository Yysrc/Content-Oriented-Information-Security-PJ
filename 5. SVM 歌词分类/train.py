# train
import jieba
import os
import joblib
from gensim import corpora
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer


# 读取所有文本信息，生成文档列表
def load_data():
    documents = []
    label = []
    # 读取每个子目录下的文本文件
    subdirs = os.walk('data/train')
    for root, _, files in subdirs:
        for file in files:
            f = open(root+os.sep+file, "r", encoding="utf-8")   # os.sep 文件分隔符
            filecontent = f.read()
            documents.append(filecontent)
            label.append(root[root.rindex("\\")+1:])            # 子目录名称作为类别标签
    return documents, label


# 预处理：分词、停用词过滤、词频过滤、特征选择
def preprocess(documents):
    stoplist = open('stopword.txt', 'r', encoding="utf-8").readlines()
    stoplist = set(w.strip() for w in stoplist)                             # 去重，删除两端空白符
    
    # 分词、去停用词
    train_data = []
    for document in documents:
        doc = []
        for w in list(jieba.cut(document, cut_all=True)):
            if len(w) > 1 and w not in stoplist:
                doc.append(w)
        train_data.append(doc)

    dictionary = corpora.Dictionary(train_data)                             # 生成词典，为每个词分配一个 id
    dictionary.filter_extremes(no_below=3, no_above=1.0, keep_n=1000)       # 按出现次数去掉一些词
    return train_data, dictionary


# 训练 svm 分类器：构造 TFIDF 矩阵、SVM 参数拟合
def train_svm(train_data, dictionary, train_tags):
    traindata = []
    dlist = list(dictionary.values())

    for l in train_data:
        words = ""
        for w in l:
            if w in dlist:
                words = words + w + " "
        traindata.append(words)

    v = TfidfVectorizer()
    tdata = v.fit_transform(traindata)

    svc = svm.SVC(kernel='rbf', gamma='auto')
    svc.fit(tdata, train_tags)
    return svc


if __name__ == '__main__':
    documents, label = load_data()
    train_data, dictionary = preprocess(documents)
    
    svm = train_svm(train_data, dictionary, label)

    dictionary.save("classifier.dict")
    joblib.dump(svm, "svm.model")
    print("训练完成！")
