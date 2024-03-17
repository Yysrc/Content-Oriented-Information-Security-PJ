import jieba
import wordcloud
import imageio
import os
from snownlp import SnowNLP
import matplotlib.pyplot as plt

#装载停用词
f = open("stopword_comment.txt",encoding='UTF8')
fl = f.readlines()
stoplist = []
for line in fl:
  stoplist.append(line.strip('\n'))
f.close()


#统计词频的字典
wordfreq = dict()

with open('comment.txt', encoding='utf-8') as f:
    t = f.read()

#切分、停用词过滤、统计词频
for w in list(jieba.cut(t, cut_all=False)):
   if len(w) > 1 and w not in stoplist:
     if w not in wordfreq:
        wordfreq[w] = 1
     else:
        wordfreq[w] = wordfreq[w] + 1

# 词云图形状
#mask = imageio.imread('shape.png')

# 绘制词云图
w = wordcloud.WordCloud(
    width=2000, 
    height=1400,
    font_path="msyh.ttc",
    # colormap='cool',
    # mask=mask,
    background_color='white')

# 将词组变量txt导入词云对象w中并保存
w.generate_from_frequencies(wordfreq)
w.to_file('comment_analyse.png')





# 情感分析
comments = t.split('\n')

positive = []
neutral = []
negative = []
total = 0


f = open('positive.txt', encoding='UTF8')
fl = f.readlines()
positive_word = []
for line in fl:
    positive_word.append(line.strip('\n'))
f.close()


f = open('negative.txt', encoding='UTF8')
fl = f.readlines()
negative_word = []
for line in fl:
    negative_word.append(line.strip('\n'))
f.close()


# 逐条评论分析情感倾向
for comment in comments:
    comment = comment.split('#')[2]
    total += 1
    flag = 0

    for w in list(jieba.cut(comment, cut_all=False)):
        if len(w) > 1:
            if w in negative_word:
                negative.append(comment)
                flag = 1
                break
            elif w in positive_word:
                positive.append(comment)
                flag = 1
                break
    
    if flag == 0:
       neutral.append(comment)

    # if(len(comment)):
    #     s = SnowNLP(comment)
    #     # 评论得分
    #     score = s.sentiments
    #     # 统计
    #     if score > 0.9:
    #         positive.append(comment)
    #     elif score < 0.5:
    #         negative.append(comment)
    #     else:
    #         neutral.append(comment)
print('\n', positive,"\n", neutral, '\n', negative, '\n')

print('\npositive: ', len(positive)/total, 
      '\nneutral: ', len(neutral)/total,
      '\nnegative: ', len(negative)/total)



# 数据
labels = ['positive', 'neutral', 'negative']
sizes = [len(positive)/total, len(neutral)/total, len(negative)/total]  # 每个类别的大小
colors = ['#ff9999', '#66b3ff', '#99ff99']
explode = (0.1, 0, 0)  # 第一个类别会被突出显示

# 画饼状图
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')

# 保存图形为PNG文件
plt.savefig('attitude.png')

plt.show()
