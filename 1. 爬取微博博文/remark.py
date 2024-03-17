# 爬取微博某个话题下的全部博文
import requests, re
import time
import csv

comments_ID = []


# 爬取该主题首页每个博文的ID，以便接下来打开每个网页，找到具体的内容。因为对于简单的博文，可能在首页就能显示全部内容，但大多数都是要打开才能看到具体内容的。
def get_title_id():
    Headers = {
    'Cookie': "XSRF-TOKEN=7zeEXABL1ve44uenbxiXKsFC; _s_tentry=weibo.com; Apache=7510325427984.301.1701593148976; SINAGLOBAL=7510325427984.301.1701593148976; ULV=1701593149006:1:1:1:7510325427984.301.1701593148976:; login_sid_t=0dedc9381c04c8112be070a5151db7a9; cross_origin_proto=SSL; wb_view_log=1280*7201.5; SUB=_2A25IaDwpDeRhGeFJ61sT9yvNyjuIHXVrBDHhrDV8PUNbmtB-LRakkW9NfLOcCRrFz5Lz9qh3M-UnVVOSIJPe6FFt; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWg14ooKKRIjMOFJUhBGI-b5JpX5KzhUgL.FoMNeh.ES0-peKM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNS054eoMfeK2N; ALF=1733132281; SSOLoginState=1701596281; WBPSESS=g9agOl3ndAzdQ_rnhcI560hT-AZd7z6EADI4OlTh864l6Lh3L5yafR6bNoHBGBdSOkbpiHLg6NTTw9TwqG92zBZZPlbzA5tlAPClqG_qApcNAhulMa_yUDn_SDwZQVsIFPfrRMt6_TWyGLh7BJ50QA==",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    'Referer':"https://s.weibo.com/"
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


# 爬取该主题下每个博文的详细内容
def spider_title(comment_ID):
    Headers = {
    'Cookie': "_T_WM=50481781298; WEIBOCN_FROM=1110006030; XSRF-TOKEN=7abe66; MLOGIN=1; SCF=Auy1xNZZrwV5nq5x7lcCNvL6NwkUx1Tlt85YBbbyxqLAYL6jTXD5DWSlJmxV0cOWXfXC8_qlCwgcdIconhQa9V0.; SUB=_2A25IaBFSDeRhGeFJ61sT9yvNyjuIHXVrBCyarDV6PUJbktAGLRT_kW1NfLOcCU1lNPlwd2oYs8H798AiTIwNeeDE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWg14ooKKRIjMOFJUhBGI-b5JpX5K-hUgL.FoMNeh.ES0-peKM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNS054eoMfeK2N; SSOLoginState=1701601538; ALF=1704193538; mweibo_short_token=f9b262602b; M_WEIBOCN_PARAMS=oid%3D4811862867187053%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253Dai%25E5%2588%259B%25E4%25BD%259C%25E4%25BC%259A%25E6%2598%25AF%25E5%258D%258E%25E8%25AF%25AD%25E4%25B9%2590%25E5%259D%259B%25E7%259A%2584%25E6%2596%25B0%25E5%2587%25BA%25E8%25B7%25AF%25E5%2590%2597%26fid%3D100103type%253D1%2526q%253Dai%25E5%2588%259B%25E4%25BD%259C%25E4%25BC%259A%25E6%2598%25AF%25E5%258D%258E%25E8%25AF%25AD%25E4%25B9%2590%25E5%259D%259B%25E7%259A%2584%25E6%2596%25B0%25E5%2587%25BA%25E8%25B7%25AF%25E5%2590%2597%26uicode%3D10000011",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    'Referer':"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3Dai%E5%88%9B%E4%BD%9C%E4%BC%9A%E6%98%AF%E5%8D%8E%E8%AF%AD%E4%B9%90%E5%9D%9B%E7%9A%84%E6%96%B0%E5%87%BA%E8%B7%AF%E5%90%97"
    }

    article_url = 'https://m.weibo.cn/detail/' + comment_ID
    print("article_url = ", article_url)
    time.sleep(1)

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
    
    except:
        print('博文网页解析错误，或微博不存在或暂无查看权限！')
        pass

# 存取的是微博博文的信息（不包含评论）
path ='D:/pythonProject/reptile/music/weibo_content.csv'
# 如果没有，就新建一个excel文件
csvfile = open(path, 'a', newline='', encoding='utf-8-sig')
writer = csv.writer(csvfile)

# 只爬取微博特定话题下相关博文的信息
writer.writerow(('楼主ID','楼主昵称', '楼主性别', '话题内容'))
get_title_id()
for comment_ID in comments_ID:
    spider_title(comment_ID)

