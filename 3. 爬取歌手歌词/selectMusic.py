# 爬取网易云音乐某个歌手的所有歌曲到多个.txt文件中
import sys
sys.setrecursionlimit(10000000) #设置递归深度
import requests
from lxml import etree
import json
import re
import operator
from functools import reduce
import os

UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
Headers = {
    'User-agent': UA
}

# 定义CrawlerLyric类，将所有函数放在类中
class CrawlerLyric:
    # 初始化对象
    def __init__(self, singer_name, singer_id):
        self.singer_name = singer_name 
        self.singer_id = singer_id
    
    # 已知“歌手-热门专辑”网页的url，获取该网页；已知某专辑的url，获取该网页
    def get_url_html(self, url):
        with requests.Session() as session:
            response = session.get(url, headers = Headers)
            text = response.text
            # text是包含HTML内容的字符串,etree.HTML()将HTML文本解析为一个ElementTree对象，然后才能使用XPath或其他方式提取文档中的内容
            html = etree.HTML(text)
        return html
    
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

    # 已知专辑网页html，获得每张专辑的id和专辑名 
    def get_album(self, html):
        album_ids = html.xpath("//ul[@id='m-song-module']/li/p/a/@href")
        album_ids = [ids.split('=')[-1] for ids in album_ids]
        album_names = html.xpath("//ul[@id='m-song-module']/li/p/a/text()")
        return album_ids, album_names

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
        return 

if __name__ == "__main__":
    a = CrawlerLyric('邓丽君','7570')
    a.get_all_song_lyric()
