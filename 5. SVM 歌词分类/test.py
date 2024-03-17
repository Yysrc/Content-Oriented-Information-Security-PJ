# test
import jieba
import os
import joblib
from gensim import corpora
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


"""
读取所有文本信息，生成文档列表.
测试样本位于列表的前面，测试样本个数与label大小一致
包含训练集，因IDF的计算与训练集有关
"""
def load_data():
    documents = []
    label = []

    # 读取每个 testdir 子目录下的文本文件
    subdirs = os.walk('data/test')
    for root, _, files in subdirs:
        for file in files:
            f = open(root+os.sep+file, "r", encoding="utf-8")
            filecontent = f.read()
            documents.append(filecontent)
            label.append(root[root.rindex("\\")+1:])   # 子目录名称作为类别标签

    # 读取每个 trainsdir 子目录下的文本文件
    subdirs = os.walk('data/train')
    for root, _, files in subdirs:
        for file in files:
            f = open(root+os.sep+file, "r", encoding="utf-8")
            filecontent = f.read()
            documents.append(filecontent)               # 训练集的内容承接在测试集后边

    return documents, label


# 预处理：分词、特征词过滤，生成新的文档列表
def preprocess(documents, dictionary):
    stoplist = open('stopword.txt', 'r', encoding="utf-8").readlines()
    stoplist = set(w.strip() for w in stoplist)                             # 去重，删除两端空白符
    dclist = list(dictionary.values())
    
    # 分词、去停用词
    dataset = []
    for document in documents:
        doc = []
        for w in list(jieba.cut(document, cut_all=True)):
            if w in dclist and w not in stoplist:
                doc.append(w)
        dataset.append(doc)
    return dataset


# 分类
def svm_classify(svm, dataset, dictionary, test_tags):
    data = []
    testresult = []
    dlist = list(dictionary.values())
    
    for l in dataset:
        words = ""
        for w in l:
            if w in dlist:
                words = words + w + " "
        data.append(words)
            
    # 把文档集（由空格隔开的词汇序列组成的文档）转换成为 tfidf 向量
    v = TfidfVectorizer()
    tdata = v.fit_transform(data)

    correct = 0
    # 获取测试样本（待分类的眼本），输出分类结果
    for i in range(len(test_tags)):
        test_X = tdata[i]
        r = svm.predict(test_X)     # 此处 test_X 为特征集
        testresult.append(r[0])
        if r[0] == test_tags[i]:
            correct += 1

    #性能评估
    cm = confusion_matrix(test_tags, testresult)
    print(cm)
    target_names = ['崔健', '邓丽君', '毛不易']
    print(classification_report(test_tags, testresult, target_names=target_names))
    print("正确率 = " + str(correct/len(test_tags)))
    return


if __name__ == '__main__':
    svm = joblib.load("svm.model")
    dictionary = corpora.Dictionary.load('classifier.dict')

    documents, label = load_data()

    dataset = preprocess(documents, dictionary)
    svm_classify(svm, dataset, dictionary, label)
    print("分类完成！")
