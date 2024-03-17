import os
import jieba
import matplotlib.pyplot as plt
from gensim import corpora
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE


def load_data():
    documents = []
    label = []
    subdirs = os.walk('data')                                       # 读取每个子目录下的文本文件
    for root, _, files in subdirs:
        for file in files:
            f = open(root + os.sep + file, "r", encoding="utf-8")   # os.sep 文件分隔符
            filecontent = f.read()
            documents.append(filecontent)
            label.append(root[root.rindex("\\") + 1:])              # 子目录名称作为类别标签
    return documents, label


# 预处理：分词、停用词过滤、词频过滤、特征选择
def preprocess(documents):
    stoplist = open('stopword.txt', 'r', encoding="utf-8").readlines()
    stoplist = set(w.strip() for w in stoplist)                             # 去重，删除两端空白符
    dataset = []
    for document in documents:
        doc = []
        for w in list(jieba.cut(document, cut_all=True)):
            if len(w) > 1 and w not in stoplist:
                doc.append(w)
        dataset.append(doc)
    dictionary = corpora.Dictionary(dataset)                                # 生成词典，为每个词分配一个 id
    dictionary.filter_extremes(no_below=3, no_above=1.0, keep_n=1000)       # 按出现次数去掉一些词
    return dataset, dictionary


def tfidf(dataset, dictionary):
    sets = []
    dlist = list(dictionary.values())
    for l in dataset:
        words = ""
        for w in l:
            if w in dlist:
                words = words + w + " "
        sets.append(words)

    v = TfidfVectorizer()
    data_array = v.fit_transform(sets).toarray()
    return data_array


def clustering(data_array, label):
    tsne = TSNE(n_components=2)
    result = tsne.fit_transform(data_array)
    k = KMeans(n_clusters=2, n_init='auto').fit(result)

    correct = 0
    for index, klabel in enumerate(k.labels_):
        if (label[index] == '崔健' and klabel == 1) or (label[index] == '邓丽君' and klabel == 0):
            correct += 1
    accuracy = correct / 80
    if accuracy < 0.5:
        accuracy = 1 - accuracy

    sort0 = result[k.labels_ == 0]
    sort1 = result[k.labels_ == 1]

    plt.scatter(sort0[:, 0], sort0[:, 1], c="salmon", s=15)
    plt.scatter(sort1[:, 0], sort1[:, 1], c="teal", s=15)
    plt.title('inertia: ' + '{:.2f}'.format(k.inertia_) + '     accuracy: ' + str(accuracy))
    plt.xticks([])
    plt.yticks([])
    plt.show()


if __name__ == '__main__':
    documents, label = load_data()
    dataset, dictionary = preprocess(documents)
    data_array = tfidf(dataset, dictionary)
    clustering(data_array, label)
