# AI 创作是华语乐坛的新出路吗

杨莹		余雪		黄权锋		杨乙



****



## 目录

- [分工](# 分工)
- [选题背景](# 选题背景)
- [从微博博文看 AI 歌词创作](# 从微博博文看 AI 歌词创作)
  - [爬取微博博文](# 爬取微博博文)
  - [博文词云图与情感分析](# 博文词云图与情感分析)
- [从原创歌词看 AI 歌词创作](# 从原创歌词看 AI 歌词创作)
  - [爬取歌手歌词](# 爬取歌手歌词)
  - [绘制歌词词云图](# 绘制歌词词云图)
- [歌手风格与歌词意象对比分析](# 歌手风格与歌词意象对比分析)
  - [SVM 歌词分类](# SVM 歌词分类)
  - [微调预训练 bert 单句歌词分类](# 微调预训练 bert 单句歌词分类)
  - [KMeans 歌词聚类](# KMeans 歌词聚类)
- [基于 RNN 的歌词生成](# 基于 RNN 的歌词生成)
- [总结](# 总结)



****



## 分工

|                              | 杨莹 | 余雪 | 黄权锋 | 杨乙 |
| :--------------------------: | :--: | :--: | :----: | :--: |
|         爬取微博博文         |      |  √   |        |      |
|     博文词云图与情感分析     |  √   |      |        |      |
|         爬取歌手歌词         |      |  √   |        |      |
|        绘制歌词词云图        |  √   |      |        |      |
|         SVM 歌词分类         |      |      |        |  √   |
| 微调预训练 bert 单句歌词分类 |      |      |   √    |      |
|       KMeans 歌词聚类        |      |      |        |  √   |
|     基于 RNN 的歌词生成      |      |      |        |  √   |
|           PPT 制作           |      |      |        |  √   |
|             报告             |  √   |  √   |   √    |  √   |
|             展示             |  √   |  √   |   √    |  √   |



****



## 选题背景

近年来 AI 发展迅猛，新技术层出不穷，已经应用到我们生活的方方面面。其中，使用 AI 创作歌词既新奇又有趣，备受大家关注，在微博上也掀起了热烈的讨论。3unshine 组合的 Cindy 就在不久前发布了一首由 AI 创作的新歌《今年中秋不调休》，歌词吐槽了我们生活中随处可见的卷王们：“今年中秋不调休，想去太空里遨游，人非 AI 不能无休地工作，你的生命被允许犯错。”

看起来还挺通顺而且有意思的！那么面对着华语乐坛知名歌手的逐渐老去，年轻一辈创作的口水歌层出不穷，值此青黄不接之时，我们不禁期待：AI 创作会是华语乐坛的新出路吗？



****



## 从微博博文看 AI 歌词创作

在微博上我们发现：许多网友对 AI 歌词创作发表了自己的观点。通过爬取带有相关词条的博文，我们对网友观点进行汇总，通过绘制词云图、进行情感分析等对这些评论进行详细探索。



### 爬取微博博文

我们对微博话题 “AI 创作会是华语乐坛的新出路吗” 下的全部博文进行爬取（出于信息有效性考虑，我们只爬取了全部博文而未爬取评论）同时，由于微博接口爬取数量的限制，我们采取直接编写爬虫程序的方法收集数据。

原理：通过指定话题在网页版微博下的 url 获取所有具体博文的 ID 列表，基于 ID 构造每个博文独一无二的 url，和移动端微博交互获取博文。其中，使用 cookies 记录用户状态。

1. `get_title_id()` 函数：通过 `requests.get()`函数获取该话题所在页面，在网页源代码中找到定位博文 ID 的规律后，借助 re 模块进行正则匹配获取所有 ID 的列表：

   ```python
   # 爬取该主题首页每个博文的ID，以便接下来打开每个网页，找到具体的内容
   # 因为在简单的博文中，可能在首页就能显示全部内容，但大多数都是要打开才能看到具体内容的。
   def get_title_id():
       Headers = {		# 具体字符串详见代码
       'Cookie':
       'user-agent':
       'Referer':
       }
   
       for Page in range(1, 7):  # 每个页面大约有10个话题
           time.sleep(1)
           # 该链接通过抓包获得
           remark_url = "https://s.weibo.com/weibo?q=ai%E5%88%9B%E4%BD%9C%E4%BC%9A%E6%98%AF%E5%8D%8E%E8%AF%AD%E4%B9%90%E5%9D%9B%E7%9A%84%E6%96%B0%E5%87%BA%E8%B7%AF%E5%90%97&page=" + str(Page)
           response = requests.get(url=remark_url, headers=Headers)
           try:
               text = response.text
               # 与mid进行匹配
               comment_ID = re.findall('(?<=mid=")\d{16}', text)
               # 把新找到的一个ID加入到列表中
               comments_ID.extend(comment_ID)
           except:
               print(Page,"页id获取有误!")
       print(comments_ID)
       
   ```

2. `spider_title(comment_ID)` 函数：爬取该主题下每个博文的详细内容。由于我们观察到微博移动端每个博文url的构造规律极为简单，故采用该平台爬取博文：

   ```python
   article_url = 'https://m.weibo.cn/detail/' + comment_ID
   ```
   
   同样在网页源代码中找到定位具体博文 “话题内容”、“楼主性别”、“楼主昵称” 等的规律后，借助 re 模块进行正则匹配来获取相关内容，并写入 csv 文件中：
   
   ```python
       try:
           html_text = requests.get(url=article_url, headers=Headers).text
           # 楼主ID
           title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
           
           # 楼主昵称
           title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
   
           # 楼主性别
           title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
           
           # 话题内容
           find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
           title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)  # 正则匹配掉html标签
   
           # position是记录
           position = (title_user_id, title_user_NicName, title_user_gender, title_text)
           
           # 写入数据
           writer.writerow((position))
           print('写入博文信息数据成功！')
   ```




### 博文词云图与情感分析

首先装载停用词：

```python
# 装载停用词
f = open("stopword_comment.txt",encoding='UTF8')
fl = f.readlines()
stoplist = []
for line in fl:
  	stoplist.append(line.strip('\n'))
f.close()
```

定义一个词典，用于统计词频。对所有评论进行切分，如果切分出的词长度大于 1 且不在停用词中，则将它加入词典（或词典中对应词频数加一）：

```python
# 统计词频的字典
wordfreq = dict()
with open('comment.txt', encoding='utf-8') as f:
    t = f.read()

# 切分、停用词过滤、统计词频
for w in list(jieba.cut(t, cut_all=False)):
   	if len(w) > 1 and w not in stoplist:
     	if w not in wordfreq:
        	wordfreq[w] = 1
     	else:
        	wordfreq[w] = wordfreq[w] + 1
```

定义词云图的参数，包括长、宽、字体、背景颜色等，然后生成词云图并保存：

```python
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
```

得到词云图如下：

<img src="D:\Desktop\报告图片\报告.png" alt="报告" style="zoom:33%;" />

词云图中比较明显的词包括：“AI”、“新出路”、“发展”、“未来”、“歌曲”，揭示了讨论的主题；其中有一些积极的情感特征，比如：“厉害”、“惊艳”、“好听”、“优秀”、“期待”；有一些比较负面的词语，比如：“枯竭”、“依赖”、“大同小异”、“太卷”、“魔性”；也有一些只是描述事实，没有明显情感特征的词。

根据词云图可以直观地看到大多数网友还是支持 AI 创作的。接下来我们对这些评论进行进一步的处理：通过情感分析将评论分类，来观察持有不同态度的人的观点，以及他们的比重。

准备工作：两个 txt 文件，positive.txt 和 negative.txt，分别保存一些积极的词和消极的词，用来判断一个评论是积极的还是消极的（由于中性的词很多很杂，这里不做定义，只将不是积极的、也不是消极的评论都定义为中性的）。positive.txt 中包含的词汇有 “不错”、“新趋势”、“趋势”、“惊艳”、“优秀”、“喜欢” 等；negative.txt 中包含的词汇有 “但是”、“大同小异”、“不会”、“辅助”、“担心” 等。

首先定义一些变量。`comments` 是一个 `list`，其中每一项是一条评论：

```python
# 情感分析
comments = t.split('\n')

positive = []
neutral = []
negative = []
total = 0
```

然后打开 positive.txt，将 `positive_word` 读出来，类似地将 `negative_word` 读出来：

```python
f = open('positive.txt', encoding='UTF8')
fl = f.readlines()
positive_word = []
for line in fl:
    positive_word.append(line.strip('\n'))
f.close()
```

逐条评论分析情感倾向。由于我们爬出来的评论的特征是 `#……#comment#……#`，所以需要选出真正的评论部分。将评论切分后，判断其中有没有消极词汇，如果没有再判断是否有积极词汇，如果都没有则为中性评论（由于评论都较短，可以认为每条评论只有一种情感倾向）：

```python
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
```

最后计算各类评论在总体中的占比，并画饼状图：

```python
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
```

得到饼状图：

<img src="D:\Desktop\报告图片\bing.png" alt="bing" style="zoom: 50%;" />

由饼状图我们分析得到：持有积极态度的人数较多，占五成；中立占三成，消极基本持平，分别占两成。下面依次查看不同态度对应的评论：

**正面评论：**

- 从来没有想到，AI 还能给我们带来了音乐了呀，未来的音乐会变成什么样子的呢？也是非常期待
- 每一个人听完这首歌都有一种不一样的体验，不得不佩服现在 AI 的能力
- 不得不说人工智能发展的速度确实是很快的，现在的智能都是越来越厉害了
- 现在的 AI 也太优秀了，做出来的歌曲我们都特别喜欢，希望以后给我们带来更多动听的歌曲

**中立评论：**

- 这个曲风还真的是有一点点的魔性，我觉得挺好玩的，以后说不定还会有 AI 创作出现
- 不得不说现在的 Cindy 真的越来越自信了，这歌还是挺好听的，或许有可能会是新出路吧
- 人总会有灵感枯竭的时候的，所以 ai 创作未尝不是一条新的出路
- 当人的创作进入瓶颈期的时候，或许就需要 ai 的作用了

**负面评论：**

- 使用 AI 辅助我们创作确实是一个很好的办法，但是如果大家都用的话，那创作出来的歌不都是会差不多吗
- 我觉得确实可以帮忙有灵感，但是我还是更喜欢歌手创作哎
- 虽然AI确实在生活中帮到了我们很多，但是也不能完全依靠吧，这样我感觉只有大同小异了
- 现在科技已经可以到达这个地步了吗？我有点担心我以后还能不能找到工作了

总而言之，正面的评论对 AI 作词表示肯定，感叹 AI 发展的速度，并对未来 AI 的发展抱有期待；中立的评论给出了一定的肯定，但对 AI 是否是新出路的问题持有观望态度；而负面的评论认为更加喜欢歌手的创作，或是担心 AI 发展过于迅速，挤占就业市场。



****



## 从原创歌词看 AI 歌词创作

通过前面对网友观点的汇总和分析，我们发现：对 AI 创作持鼓励、中立、乃至不看好的网友都不在少数，那么 AI 会是华语乐坛的新出路吗？我们将通过歌曲歌词分类、歌曲聚类等方法分析代表原创歌手的歌词风格，并训练一个简单的 AI 模型来看 AI 创作和真实歌手创作的差别，进而探索 “AI 创作会是华语乐坛的新出路吗” 这个问题的答案。



### 爬取歌手歌词

为获取原创歌手创作过的所有歌曲的歌词，我们通过网易云音乐爬取了12位典型歌手的全部歌词。

原理：观察网页源代码及 url 构造规律，我们决定采用 “获取歌手所有专辑 ID —— 获取全部专辑的所有歌曲 ID —— 爬取歌曲” 的思路爬虫。

1. 定义类 `CrawlerLyric` 类：我们将所有函数都放在 `CrawlerLyric` 中，并设置初始化函数：

   ```python
   # 定义CrawlerLyric类，将所有函数放在类中
   class CrawlerLyric:
       # 初始化对象
       def __init__(self, singer_name, singer_id):
           self.singer_name = singer_name 
           self.singer_id = singer_id
           
   ```

2. `get_url_html()` 函数：已知歌手 ID，我们可以构造出 “某歌手 - 热门专辑” 网页的 url，通过 `session.get()` 获取专辑页面（歌手 ID 可以采用直接打开该歌手网页，在 url 上复制的方法，也可再次采用爬虫的方法获取所有歌手的 ID，在本方案中，由于我们需要只需分析代表歌，因此采取法 1）。

   之后观察网页源代码的结构，通过 xpath 定位专辑 ID 和专辑名所在位置，获取专辑 ID 和专辑名列表：

   ```python
       # 已知专辑网页html，获得每张专辑的id和专辑名 
       def get_album(self, html):
           album_ids = html.xpath("//ul[@id='m-song-module']/li/p/a/@href")
           album_ids = [ids.split('=')[-1] for ids in album_ids]
           album_names = html.xpath("//ul[@id='m-song-module']/li/p/a/text()")
           return album_ids, album_names
   
   ```

3. `get_all_song_id()`：已知专辑 ID，构造专辑对应网页的 url，通过爬虫获取所有网页。并观察网页源代码的结构，通过 xpath 定位歌曲 ID 所在位置,获取所有歌曲的 ID 列表：

   ```python
       # 已获取某歌手所有专辑的id列表，获取所有歌曲id列表
       def get_all_song_id(self, album_ids):
           # 初始化两个空列表
           all_song_ids, all_song_names = [], []
           for album_id in album_ids:
               an_album_url = "https://music.163.com/album?id=" + str(album_id)
               # 获取该专辑的网页
               response = requests.get(an_album_url, headers = Headers)
               text = response.text
               html= etree.HTML(text)
               # 根据源网页结构，定位到每首歌的id
               album_song_ids = html.xpath("//ul[@class='f-hide']/li/a/@href")
               # 进行分割，实际id只为数字部分
               album_song_ids = [ids.split('=')[-1] for ids in album_song_ids]
               # 根据源网页结构，定位到每首歌的歌名
               album_song_names = html.xpath("//ul[@class='f-hide']/li/a/text()")
               # 将上文获取的歌曲id和名字加入二维列表中
               all_song_ids.append(album_song_ids)
               all_song_names.append(album_song_names)  
           return all_song_ids, all_song_names
       
   ```

4. `get_lyric()` 函数：已知歌曲 ID 列表，我们根据歌曲 url 的构造规律，构造出歌曲的 url，获取对应网页后，通过 re 模块的正则匹配获得歌词。重点在于歌曲对应网页的格式为 json，所以必须采用对应的函数进行解析：

   ```python
       # 已知歌曲的url，获取歌词（该url返回的是json数据格式的结果，因此需要通过python的json模块解析结果）    
       def get_lyric(self, song_id):
           # 网易云音乐的歌词在网页上是不能直接爬取的，我们可以通过接口来得到歌曲的歌词(加最后的后缀)：http://music.163.com/api/song/lyric?id=song_id&lv=1&kv=1&tv=-1
           song_url = 'http://music.163.com/api/song/lyric?id='+str(song_id)+'&lv=1&kv=1&tv=-1'
           response = requests.get(song_url, headers = Headers)
           text = response.text
           json_obj = json.loads(text)
           initial_lyric = json_obj['lrc'].get('lyric', '')
           regex = re.compile(r'\[.*\]')
           final_lyric = re.sub(regex, '', initial_lyric).strip()
           return final_lyric
       
   ```

5. `get_all_song_lyric()`：顺序调用前面提到的所有函数，得到某个歌手的所有歌词，并将每首歌词写入一个 txt 文件中。为了训练后文模型，我们改变该函数，得到 select_all.py 程序，实现将一个歌手的所有歌词写入一个 .txt 文件中：

   ```python
       # 最终需要使用的函数：已知歌手ID，返回所有歌曲的歌词
       def get_all_song_lyric(self):
           # 构造该歌手专辑页面的URL,其中limit是每页显示的专辑数量、offset是偏移量
           album_url = "https://music.163.com/artist/album?id="+str(self.singer_id)+"&limit=150&offset=0"
           # 获得专辑网页
           html_album = self.get_url_html(album_url)
           # 由专辑网页获得每张专辑的id和专辑名
           album_ids, album_names = self.get_album(html_album)
           # 由专辑id获取所有歌曲id和歌曲名
           all_song_ids, all_song_names = self.get_all_song_id(album_ids)
           
           # ids在列表的列表中，合成一个列表
           all_song_ids = reduce(operator.add, all_song_ids)
           all_song_names = reduce(operator.add, all_song_names)
           
           path = self.singer_name 
           # 创建文件夹
           os.makedirs(path)
           # 打开文件夹
           os.chdir(path)
   
           for song_id, song_name in zip(all_song_ids, all_song_names):  
               lyric = self.get_lyric(song_id)
               try:
                   with open('{}.txt'.format(song_name), 'a', encoding='utf-8')as fp:
                       fp.write(lyric)
               except Exception as e:
                   pass
           print("finish!")
   ```



### 绘制歌词词云图

我们挑选了三位歌手进行词云图绘制，由于生成过程与上文方法相似，在这里不做赘述。下面展示通过得到的词云图制作的海报，并通过词云图对歌手的作词风格进行辨析。

1. 崔健：

   ![屏幕截图(46)](D:\Desktop\报告图片\屏幕截图(46).png)

   崔健的歌词中出现频率较高的有 “生活”、“明白”、“世界”、“想要”，体现出一种充满力量、激情和社会关怀的感情。我们从中可以看到崔健的风格是直白而富有表达力的，他在歌曲中表达了强烈的个人观点和对社会现象的关切。同时，他的歌词内容涵盖了广泛的主题，包括对人性、自由、梦想的追求，以及对社会不公和现实问题的反思，展现出对生活的热爱和面对困境坚韧不拔的态度。

   

2. 邓丽君：

   ![屏幕截图(47)](D:\Desktop\报告图片\屏幕截图(47).png)

   “爱情”、“忘不了”、“我俩”、“甜蜜”，给人一种温柔深情感觉。像 “春风”、“今宵”、“流水” 这些词表明她的歌词语言简洁清新，富有诗意，描写的感情的细腻而真挚。我们也可以看出她的歌词内容通常是对爱情、家庭、友谊以及人生的感悟，充满了对温暖和幸福生活的向往。

   

3. 毛不易：

   ![屏幕截图(48)](D:\Desktop\报告图片\屏幕截图(48).png)

   毛不易的关键词是 “生活”、“梦想”、“有钱”、“回答”，充满着真实的生活体验和深刻的情感，反映出他对于情感和人性的敏感洞察力。我们可以看到他的歌词语言直白质朴，不追求华丽辞藻，而更注重真实和情感共鸣，使听众能够更好地感受到歌曲所传达的情感。



****



## 歌手风格与歌词意象对比分析

我们将通过分类、聚类等方法，从创作风格和歌词意象入手，对邓丽君、崔健、毛不易这三位不同时期歌手的作品进行分析，进而更全面地理解歌手创作风格之间的差异，为后续我们探索 AI 的学习机制做好铺垫。下面我们将分别进行 SVM 歌曲分类、微调预训练 bert 单句歌词分类、KMeans 歌曲聚类分析，相信这些工作将为我们寻找最终的答案提供帮助。



### SVM 歌词分类

有效的分类工作可以反映不同歌词之间的区别，有助于分析不同歌手的风格差异。我们将选取三位不同时代、不同背景的歌手的歌词来训练分类模型。我们可以推断，分类模型在测试集上的准确率越高，歌手词风之间的差异越大。项目结构如下：

```
5. SVM 歌词分类
	│ 
	├── data
	│   └── train
	│   │   ├── 崔健		# 训练集内每位歌手各24首歌词
	│   │   ├── 邓丽君
	│   │   └── 毛不易
	│   │
	│   └── test
	│       ├── 崔健		# 测试集内每位歌手各10首歌词
	│       ├── 邓丽君
	│       └── 毛不易
	│ 
	├── classifier.dict	 # 训练集字典
   	├── stopword.txt     # 停用词列表
   	├── svm.model		 # SVM分类模型
   	├── train.py		 # 训练程序
   	└── test.py 		 # 测试程序
```

其中训练集 `train` 包含了以三位歌手姓名命名的文件夹，每个文件夹内有该歌手的 24 首作品的歌词。测试集 `test` 与训练集结构相同，每个文件内有 10 首作品。训练集和测试集的数据不重合。SVM 分类的实现方法与教材 11.3.3 大致相同，因此不作分析。具体原理详见项目代码注释。下面分析模型的测试结果。

![屏幕截图(32)](D:\Desktop\报告图片\屏幕截图(32).png)

根据输出，得到混淆矩阵：

|        | 崔健 | 邓丽君 | 毛不易 |
| :----: | :--: | :----: | :----: |
|  崔健  |  6   |   4    |   0    |
| 邓丽君 |  0   |   10   |   0    |
| 毛不易 |  0   |   2    |   8    |

表格内的数据代表了行标题歌手的所有作品中，被预测为列标题歌手作品的数目。例如，崔健的作品有 6 首预测正确，其余 4 首错误预测为邓丽君的作品。同时邓丽君的作品全部预测正确，因此可以推断邓丽君具有极为鲜明的个人风格。

此外，下面的数据可以帮助我们评估模型的性能：

|              | accuracy | recall | f1-score | support |
| :----------: | :------: | :----: | :------: | :-----: |
|     崔健     |   1.00   |  0.60  |   0.75   |   10    |
|    邓丽君    |   0.62   |  1.00  |   0.77   |   10    |
|    毛不易    |   1.00   |  0.80  |   0.89   |   10    |
|  Macro avg   |   0.88   |  0.80  |   0.80   |   30    |
| Weighted avg |   0.88   |  0.80  |   0.80   |   30    |

测试集内的文件数目相同，所以 Macro avg 和 Weighted avg 相同，同时，得到总体预测准确率：0.80。这说明不同歌手的歌词之间确实存在着比较明显的差异。



### 微调预训练 bert 单句歌词分类

上面的分类方法准确率不算很高，而且实现的是对于整首歌词的分类，下面我们将基于微调预训练 bert 模型，实现单句歌词分类。

#### 准备工作

- 从 git 上下载预训练的 BERT 模型（BERT 是一个由 Google 开发的自然语言处理模型，他基于 Transformer 架构，专门用于处理自然语言文本，我们选取的是 bert 的一个在中文语料上微调的 “bert-base-chinese” 模型）

- 在本地配置conda环境以及Transformer架构

- 获取12位歌手的歌词

（本次实验的模型参考了 https://github.com/huggingface/transformers/tree/main）

#### train_classification

1. **数据处理：**

   ```python
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
   ```

   在爬取下来的歌词中，文件的组织结构是，根目录下有多个文件夹，每个文件夹以歌手的名字作为文件夹名，文件夹内部有对应的 txt 文件，一首歌对应一个 txt 文件。于是我选择传入 `load_data` 方法中的参数是根文件夹，我们首先遍历该文件夹，对该文件夹中的每个子文件夹再进行遍历，只处理以 .txt 为拓展名的文件。以 utf-8 的编码方式打开该文件，并一行一行对歌词进行处理

   ​		因为每首歌词中，都存在着如 “作曲：”、“编曲：” 等等，这些并不属于歌手风格的一部分，因此我设置了规则对每句歌词进行过滤，行内包含着冒号的行都删去。由于要定义输入和输出，我们选择对每行歌词都打上 tag，因为每首歌词所在文件夹的名字正好就是歌手名，直接取路径中的最后一部分，为了代码有可移植性，因此每首歌词的 labels 都要用歌手的名字乘以歌词的行数。最后，函数返回该文件夹所有的语料以及对应的标签。

2. **训练过程：**

   ```python
   import os
   from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
   from datasets import Dataset
   
   
   if __name__ == "__main__":
       singers = ["陈奕迅", "刀郎", "周杰伦", "孙燕姿", "小虎队",
                  "崔健", "王菲", "罗大佑", "薛之谦", "许嵩", "邓丽君", "邓紫
   ```

   **文本预处理**

   首先，我们组选取了这 12 位相对来说风格各异的歌手

   ```python
       id2label = {idx: label for idx, label in enumerate(singers)}
       label2id = {label: idx for idx, label in enumerate(singers)}
   ```

   其次，构建两个字典，分别实现从索引映射到标签以及从标签映射到索引的操作，例如，`id2label[0]`可以得到索引为 0 的歌手标签，而 `label2id['歌手A'] `可以得到标签为 `歌手A` 的索引。这样的操作是为了 BERT 模型在训练时构建索引和名称之间的双向映射，便于训练以及评估。

   ```python
       train_dicts = ["./music/a song in a text/" + name for name in singers]
       docs, labels = [], []
       for dic in train_dicts:
           doc, label = load_data(dic)
           docs += doc
           labels += label
   		
   ```

   然后，将所有歌手的文件夹路径加入到列表 `train_dicts` 中。并通过便利所有文件夹中的文件，利用 `load_data` 构建语料

   ```python
       tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
      
       tokenized_docs = tokenizer(
           docs, padding=True, truncation=True, max_length=512)
       #将歌词分词标记化，设置最长的歌词不超过512句，不到512句的进行0填充，超过的则将进行截断
       
   ```

   接着，因为 BERT 模型中，`Tokenizer` 能够对原始语料实现分词标记化，所以这里用的是 bert的一个在中文语料上微调的`bert-base-chinese` 模型，以此自动化地构造了供模型学习的语料。为了构造输入和输出的关系，tokenizer 还需要进行零填充和截断。我选取的上限是 512 句，一般歌都不会超过这个限度。

   ```python
       labels = [label2id[l] for l in labels]
     
    		dataset = Dataset.from_dict(
           {'input_ids': tokenized_docs['input_ids'], #语料部分
            'attention_mask': tokenized_docs['attention_mask'],# 告知模型哪些属于0填充，不予考虑
            'labels': labels,# 语料部分对应的标签
            })
       #生成数据集
       
       train_dataset, test_dataset = dataset.train_test_split(test_size=0.1).values()
   		#随机划分出10%作为测试集，其余作为训练集
   ```

   最后，我们根据在 singers 中的顺序来对歌手进行编号，并以此顺序构造数据集：

   数据集的语料部分就是 `'input_ids'`，`'attention_mask'` 是一个很重要的部分，因为我们前面对语料进行了零填充,而attention 机制可以告知模型哪些部分是我们零填充的结果，在训练时就不需要考虑这些部分，提高了准度和效率，`labels` 是语料部分对应的标签，这几个部分的参数构成了一个数据集。

   由于训练集和测试集不能有重合，于是从数据集中划出 10% 来作为测试集，其余的作为训练集。

   **构造模型**

   ```python
       model = BertForSequenceClassification.from_pretrained(
           "bert-base-chinese", 
           num_labels=len(singers), 
           id2label=id2label, 
           label2id=label2id
       )
       #加载模型，定义模型、分类数以及映射关系
   
   ```

   我使用了 HuggingFace 的 Transformers 库中的 `BertForSequenceClassification` 模型类，从预训练的中文 BERT 模型 `bert-base-chinese` 中创建一个用于序列分类的模型。`num_labels=len(singers)` 指定了模型输出的标签数量，表示标签的数量等于歌手（singers）的数量。`id2label=id2label` 和 `label2id=label2id` 是两个字典， 用于映射模型输出的标签索引与具体的标签名称之间的关系。前者将标签索引映射到标签名称，而后者将标签名称映射到标签索引，他们在训练和评估中能将模型输出的索引转换为实际的标签。

   ```python
           training_args = TrainingArguments(
           output_dir='./results', #训练结果的输出目录
           num_train_epochs=5, # 训练的总轮数
           per_device_train_batch_size=8, # 每个设备上的训练批次大小 
           per_device_eval_batch_size=16, # 每个设备上的评估批次大小
           warmup_steps=500,# 学习率 warmup 步数，即在这个步数内学习率逐渐增加
           weight_decay=0.01, # 权重衰减的值，用于控制模型参数的正则化，防止过拟合
           logging_dir='./logs', # 日志输出目录
       )
       
       trainer = Trainer(
           model=model,
           args=training_args,
           train_dataset=train_dataset,
           eval_dataset=test_dataset
       )
       #使用hugging face中的train进行训练，提供快速训练的库，这里对训练的参数进行了设置，并定义了trainer
   ```

   模型的训练需要定义一些参数，具体的设置如上。

   ```python
       print("Training starts\n")
       trainer.train()
       trainer.evaluate()
       #进行训练并评估模型效果
   ```

   最后开始训练并评估。

   <img src="D:\Desktop\报告图片\微信图片_20231211123104.jpg" alt="微信图片_20231211123104" style="zoom:50%;" />

   得到了这样四个 checkpoint，分别对应 500、1000、1500 和 17000 iteration，下方选取 17000 iteration 的版本来进行测试

#### inference

```python
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import torch.nn.functional as F

model = BertForSequenceClassification.from_pretrained('./results/checkpoint-1500/')
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
```

测试首先导入模型以及 tokenizer

```python
def classify_sequence(sequence):
    inputs = tokenizer(sequence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = F.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    return predicted_class, probabilities[0][predicted_class].item()
```

其次，定义了对序列的分类函数，

`inputs = tokenizer(sequence, return_tensors="pt", padding=True, truncation=True, max_length=512)` 使用一个名为 `tokenizer` 的对象对输入序列进行处理。这个 tokenizer 负责将文本数据转换为模型可以理解的格式。`return_tensors="pt"` 表示返回 PyTorch 张量。`padding=True` 和 `truncation=True` 用于对序列进行填充和截断，确保输入的序列长度不超过 512。

`with torch.no_grad()` 确保了在下面的代码中不会进行梯度计算,提高运行效率。

`outputs = model(**inputs)` 通过调用名为 `model` 的模型，将处理过的输入传递给模型进行推理。`**inputs` 表示将 `inputs` 字典中的键值对解包为关键字参数传递给模型。

由于 `outputs.logits` 包含了模型的原始输出,因此我使用 PyTorch 中的 `softmax` 函数对模型的输出进行归一化，得到每个类别的概率分布。然后通过 `argmax` 取概率最大的类别索引，作为预测的类别。

最后返回预测的类别和对应类别的概率。函数的返回类型是一个包含两个元素的元组，第一个元素是预测的类别，第二个元素是该类别的概率值。

**测试结果：**

我们选取了训练 iteration 最多的模型，这里用的是训练 17000 iteration（5 epoch）之后的模型

![微信图片_20231211123147](D:\Desktop\报告图片\微信图片_20231211123147.jpg)

可以通过更改 sequence 后的句子，喂给模型，实现对某句歌词属于哪个歌手的预测

因为测试集和训练集的划分是随机的，我们其实无法知道哪些歌词是训练集中的，但是我们可以使用一些别的歌手的歌词，来看看他们的创作风格与选取的 12 位歌手哪位更接近，如下，

![微信图片_20231211123131](D:\Desktop\报告图片\微信图片_20231211123131.jpg)

《雪》是一首新生代说唱歌手 capper 的歌曲，这一句 “可是雪飘进双眼” 更是整首歌曲中最为出圈的。我们将其喂给模型，虽然置信度明显降低，但会发现预测结果更贴近邓丽君的风格。我的推测是由于邓丽君的歌曲中包含了更多雪的意象，以及更喜欢利用自然景物来抒发自己的情感，所以才有了这样的结果。



### KMeans 歌词聚类

相比于分类，聚类方法的样本标签是未知的，我们可以对不同歌手的多篇歌词进行聚类，验证聚类效果，同样可以说明歌手之间的风格差异。K 均值聚类算法的原理是，确定类别 K 以后，选取 K 个样本作为初始类中心，通过循环，不断迭代类中心点，计算各样本到类中心点的距离，根据距离最近的原则重新归类，当类的内部距离最小，类间距离最大时，即可停止迭代。下面我们将对崔健、邓丽君两位歌手各 40 首作品（共 80 首）进行聚类，完成聚类可视化，并计算聚类结果准确率。

1. `load_data()` 函数读取 data 文件夹下某一歌手文件夹中所有歌词，生成文档列表：

   ```python
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
   ```

2. `preprocess()` 函数对文档列表进行了分词、停用词过滤、词频过滤、特征选择等预处理：

   ```python
   # 预处理：过滤分词、停用词，根据词频过滤、特征选择
   def preprocess(documents):
       stoplist = open('stopword.txt', 'r', encoding="utf-8").readlines()	# 加载停用词列表
       stoplist = set(w.strip() for w in stoplist)                         # 去重，删除两端空白符
       dataset = []														
       for document in documents:
           doc = []
           for w in list(jieba.cut(document, cut_all=True)):
               if len(w) > 1 and w not in stoplist:
                   doc.append(w)
           dataset.append(doc)												# 每首歌词分词后的列表组成的列表
       dictionary = corpora.Dictionary(dataset)                            # 生成词典，为每个词分配一个 id
       dictionary.filter_extremes(no_below=3, no_above=1.0, keep_n=1000)   # 按词频过滤掉一些词
       return dataset, dictionary
   ```

3. `tfidf()` 函数

   ```python
   def tfidf(dataset, dictionary):
       sets = []
       dlist = list(dictionary.values())				# 将词典值转化为 list
       for l in dataset:
           words = ""
           for w in l:
               if w in dlist:
                   words = words + w + " "				# 每首歌内容加空格拼接成字符串
                   									# 以便后续进行 tf-idf 转化
           sets.append(words)							# 加入列表
       v = TfidfVectorizer()							# 把原始文本转化为 tf-idf 的特征矩阵
       data_array = v.fit_transform(sets).toarray()	# 注意要将 scipy.sparse._csr.csr_matrix 类型转化为
       												# numpy.ndarray 类型，以便后续进行聚类处理
       return data_array
   ```

4. `clustering()` 函数将之前得到的 `data_array` 进行聚类处理。首先使用 T-SNE 算法对 `data_array` 降维，因为原来的数据维度过高且分布稀疏，容易引发维度灾难（大部分样本间的距离会被压缩到很小的范围内，以致无法区分），降维可以改变空间维度上的稀疏分布，也便于将聚类结果在二维图片上展示：

   ```python
       tsne = TSNE(n_components=2)								# 降至 2 维
       result = tsne.fit_transform(data_array)
   ```

   使用 KMeans 方法将降维后的结果分为两个类：

   ```python
   	k = KMeans(n_clusters=2, n_init='auto').fit(result)
   ```

   接下来根据之前得到的 `label` 预测聚类准确率。对于两个类中的一个，其聚类结果的 `klabel` 可能为 0 也可能为 1。因此我们将先按照崔健的歌词聚类结果为 1、邓丽君的歌词聚类结果为 0 来计算，若计算结果小于 0.5 则进行翻转：

   ```python
       correct = 0
       for index, klabel in enumerate(k.labels_):
           if (label[index] == '崔健' and klabel == 1) or (label[index] == '邓丽君' and klabel == 0):
               correct += 1
       accuracy = correct / 80
       if accuracy < 0.5:
           accuracy = 1 - accuracy
   ```

   接下来，我们将聚类结果在二维上可视化，同时在图片上展示 `k.inertia_` 和聚类准确率。`k.inertia_` 是样本点距其最近聚类中心的平方距离之和，越小说明聚类效果越好：

   ```python
   	sort0 = result[k.labels_ == 0]
       sort1 = result[k.labels_ == 1]
   
       plt.scatter(sort0[:, 0], sort0[:, 1], c="salmon", s=15)
       plt.scatter(sort1[:, 0], sort1[:, 1], c="teal", s=15)
       plt.title('inertia: ' + '{:.2f}'.format(k.inertia_) + '     accuracy: ' + str(accuracy))
       plt.xticks([])
       plt.yticks([])
       plt.show()
   ```

   聚类可视化如下：

   <img src="D:\Desktop\报告图片\屏幕截图(36).png" alt="屏幕截图(36)" style="zoom:33%;" />

   可以看到因为样本太少，可视化效果不是很明显。inertia 值为 1426.40，聚类准确率为 0.71



通过上述分析，我们发现了不同歌手的歌词有比较明显的风格差异。所以我们得到结论，这些歌手之所以深受喜爱，就是因为他们独特的创作风格。那AI是否能形成自己的创作风格呢？



****



## 基于 RNN 的歌词生成

（注：这部分的实现参考了网站：[周杰伦发新歌了？我们一起用神经网络预测他的歌词吧 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/147960435)）

RNN 在处理序列特性的数据时表现良好，因为它每一时刻的隐藏层不仅由该时刻的输入层决定，还由上一时刻的隐藏层决定。我们将基于 RNN 实现一个语言模型，采用不同歌手的歌词进行训练，根据其预测功能实现给定前缀词的歌词自动生成。

1. `load_lyrics()` 函数：将数据集中不同的字符对应为一个数字（字符 ID）

   ```python
   def load_lyrics(signer):
       text = ''														# 数据字符串
       os.chdir('data')
       subdirs = os.walk(signer)  										# 读取每个子目录下的文本文件
       for root, _, files in subdirs:
           for file in files:
               f = open(root + os.sep + file, "r", encoding="utf-8")
               data = f.read().replace('\n', ' ').replace('\r', ' ')	# 读取文件内容，空行替换为空格
               text += data											# 连接到数据字符串
       text = text[0: min(10000, len(text))]							# 截取前 10000 个字符
       char_list = list(set(text))                                               # 索引 to 字符（列表）
       char2idx_dict = dict((char, idx) for idx, char in enumerate(char_list))   # 字符 to 索引（字典）
       idx_list = [char2idx_dict[char] for char in text]                         # 字符 to 索引（列表）
       input_size = len(char2idx_dict)                                           # 输入数目
       return char_list, char2idx_dict, input_size, idx_list
   
   ```

2. `load_lyrics_iter()` 函数：时间步选择为 5，把相邻两个输入小批量在原始序列上的位置相毗邻，每次读取小批量前将隐藏状态从计算图中分离出来

   ```python
   def load_lyrics_iter(idx_list, device, batch_size=2, step_num=5):
       batch_num = len(idx_list) // batch_size                                         # batch 数目
       epoch_num = (batch_num - 1) // step_num                                         # 轮次
       idx_tensor = torch.tensor(idx_list, dtype=torch.float32, device=device)
       idx_tensor = idx_tensor[0: batch_size * batch_num].view(batch_size, batch_num)  # reshape
       for i in range(epoch_num):
           X = idx_tensor[:, i * step_num: (i + 1) * step_num]                         # 取相邻的小批量
           Y = idx_tensor[:, i * step_num + 1: (i + 1) * step_num + 1]
           yield X, Y
           
   ```

3. `to_one_hot()` 函数：把样本变为 `one_hot` 列表，以便输入模型

   ```python
   def to_one_hot(X, input_size):
       one_hot = []
       device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
       for i in range(X.shape[1]):
           x = X[:, i].long()                                                      # 向下取整
           res = torch.zeros(x.shape[0], input_size, dtype=torch.float32, device=device)
           res.scatter_(1, x.view(-1, 1), 1)                                       # 转变为 one_hot
           one_hot.append(res)
       return torch.stack(one_hot)													# 扩张维度
   
   ```

4. `RNNModel` 类：构建 RNN 神经网络

   ```python
   class RNNModel(nn.Module):
       def __init__(self, input_size):
           super(RNNModel, self).__init__()
           self.rnn = nn.RNN(input_size=input_size, hidden_size=256)
           self.dense = nn.Linear(256, input_size)							# 全连接层
           self.input_size = input_size									# 输入大小
           self.state = None												# rnn 状态，初始为 None
   
       def forward(self, X, state):										# 前向传播
           X = to_one_hot(X, self.input_size)
           Y, self.state = self.rnn(X, state)								# 得到输出和新的状态
           Y = self.dense(Y.view(-1, Y.shape[-1]))
           return Y, self.state
           
   ```

5. `train()` 函数：训练模型，把上一步的输出和新的输入作为模型输入，重复这一过程，直到读取全部数据

   ```python
   def train(model, lyrics_iter, criterion, optimizer):
       state = None
       train_loss = 0.0
       sample_num = 0
       for X, Y in lyrics_iter:
           if state is not None:
               state = state.detach()  # 使模型参数的梯度计算只依赖一次迭代读取的小批量序列，防止梯度计算开销太大
           optimizer.zero_grad()
           (output, state) = model(X, state)   
           							# output: 形状为(num_steps * batch_size, vocab_size)
           y = torch.transpose(Y, 0, 1).contiguous().view(-1)      
           							# Y 转置后再变成长度为 batch * num_steps 的向量
           loss = criterion(output, y.long())
           loss.backward()				# 反向传播
           nn.utils.clip_grad_norm_(parameters=model.parameters(), max_norm=10, norm_type=2)
           							# 梯度裁剪，避免梯度爆炸
           optimizer.step()
           sample_num += y.shape[0]
           train_loss += loss.item() * y.shape[0]
   
       train_loss /= sample_num
       return train_loss
   
   ```

6. `generate()` 函数：把前缀词转化为 `one_hot` 向量作为输入，把向量、状态共同输入模型，得到模型的输出（也是向量和状态），根据输出预测下一个字符，直到达到循环结束条件

   ```python
   def generate(prefix, gen_len, model, char_list, char2idx_dict, device):
       state = None
       output = [char2idx_dict[prefix[0]]]
       for idx in range(gen_len + len(prefix) - 1):
           if state is not None:
               state = state.to(device)
           X = torch.tensor([output[-1]], device=device).view(1, 1)
           	# 上一时间步的输出作为当前时间步的输入
           (Y, state) = model(X, state)
           	# 下一时间步输入是前缀词字符或当前最佳预测字符
           if idx < len(prefix) - 1:
               output.append(char2idx_dict[prefix[idx + 1]])
           else:
               output.append(int(Y.argmax(dim=1).item()))
       return ''.join([char_list[idx] for idx in output])
   
   ```

7. `main()` 函数：

   ```python
   def main():
       signer = input("请输入你想训练的歌手：")
       char_list, char2idx_dict, dict_size, idx_list = load_lyrics(signer)
       epoch_num, batch_size, lr = 250, 32, 1e-3
       gen_len = 140
       step_num = 10
       prefix = input("请输入前缀词：")
   
       device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
       model = RNNModel(dict_size)
       model = model.to(device)
       criterion = nn.CrossEntropyLoss()							# 损失函数
       optimizer = torch.optim.Adam(model.parameters(), lr=lr)		# 优化器
   
       for epoch in range(epoch_num):								# 训练 250 轮次
           lyrics_iter = load_lyrics_iter(idx_list, device, batch_size, step_num)
           perplexity = train(model, lyrics_iter, criterion, optimizer)
           if epoch % 50 == 0 and epoch:							# 在 50 倍数轮次进行生成
               print('epoch %d, train_loss %f' % (epoch, perplexity))
               print('  ', generate(prefix, gen_len, model, char_list, char2idx_dict, device=device))
   
   ```



运行效果如下图：

![屏幕截图(45)](D:\Desktop\报告图片\屏幕截图(45).png)

可以观察到，随着训练轮次的增加，生成的歌词也更加完整、通顺。下面我们将前缀词选择为 “爱”，分别用三位歌手的歌词对模型进行训练，选择部分歌词进行展示：

![屏幕截图(50)](D:\Desktop\报告图片\屏幕截图(50).png)





****



## 总结

所以我们不难发现，AI 更擅长文本特征的模仿，它带来的创新是极为有限的。没有创新作为支撑，作品的风格难免雷同。因此对于我们的问题，“AI 创作会是华语乐坛的新出路吗？”，我想答案是否定的。 “创作” 一词，重点在 “创造”，其次在 “作品”。而创造力，却是人类独有 的——它源自人类思想和文化的沃土，而不是神经网络上冰冷的数字。今天的问题之所以被提出，不在于人工智能的强大，而在于华语乐坛的堕落。这样的一个华语乐坛，它的出路不是 AI，而是有创造力、有生命力的歌手；是有良心、有诚心的文化企业；是有温度、有深度的作品——给欣赏者以触动，给创作者以充实，人文关怀永远是艺术作品的核心价值。再强大的科技只能是工具，只有那个大写的 “人”，才是我们最终的目的。
