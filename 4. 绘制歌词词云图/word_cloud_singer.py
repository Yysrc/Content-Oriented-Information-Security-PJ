import jieba
import wordcloud
import imageio
import os
#from scipy.misc import imread  #这是一个处理图像的函数

#装载停用词
f = open("stopword_singer.txt",encoding='UTF8')
fl = f.readlines()
stoplist = []
for line in fl:
  stoplist.append(line.strip('\n'))
f.close()

# 列出所有歌手
root = 'target_singer'
singer_list = os.listdir(root)

# 添加歌手名到停用词列表
for singer in singer_list:
    stoplist.append(singer)


for singer in singer_list:
    # 列出这个歌手的所有歌
    path = root + '\\' + singer
    song_list = os.listdir(path)

    t = ""
    # 读取每首歌
    for song in song_list:
        with open(path + '\\' + song, encoding='utf-8') as f:
            t += f.read()
            
    #统计词频的字典
    wordfreq = dict()     
        
    # 分词
    ls = jieba.lcut(t)
    for word in ls:
        if len(word) > 1 and word not in stoplist:
            if word not in wordfreq:
                wordfreq[word] = 1
            else:
                wordfreq[word] = wordfreq[word] + 1
    
    # 词云图形状
    #mask = imageio.imread('shape.png')

    # 绘制词云图
    w = wordcloud.WordCloud(
        width=2000, 
        height=1400,
        font_path="msyh.ttc",
        colormap='spring',
       # mask=mask,
        background_color='white')

    # 将词组变量txt导入词云对象w中并保存
    w.generate_from_frequencies(wordfreq)
    w.to_file('cloud_pictures\\' + singer + '.png')