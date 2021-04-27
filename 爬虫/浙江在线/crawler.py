# -*-coding:utf-8 -*-

"""
# File       : crawler.py
# Time       ：2021/4/23 15:42
# Author     ：wassily
# version    ：python 3.7
# Description：脚本上级目录中新建data文件夹
"""
from bs4 import BeautifulSoup
import urllib.request as ur
import get_article_content as gac

# 爬取单页目录中所有文章url
def get_url(url):
    try:
        res = ur.urlopen(url=url).read()
        soup = BeautifulSoup(res, "html5lib")
        articles = {}
        for tag in soup.find_all('ul', class_='listUl'):  ## 需要内容的上级标签
        # for tag in soup.find_all('h3', class_='titTwo'): ## xjp
            # print(tag)
            for i in tag.find_all('a'):
                url = i.get('href')
                title = ''.join(i.contents)
                articles[title] = 'https:' + str(url)
        return articles
    except:
        pass

# 爬取所有目录中的所有文章的url
## pageurl是所有目录页面url的列表
def get_article_url(pageurl):
    articles = {}
    num = 1
    for i in pageurl:
        try:
            article = get_url(i)
            articles.update(article)
            print('第{}页完成'.format(num))
        except:
            pass
        num += 1
    return articles

## 保存所有文章的url
def save_url(url_file, article_urls):
    with open(url_file,'w') as file:
        for i in article_urls.items():
            file.write(str(i))
            file.write('\n')

if __name__ == '__main__':
    # headers = {
    #     'Host': 'zjnews.zjol.com.cn',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    # }   ## 没有用到请求头

    ## 首页网址
    url = 'https://zjnews.zjol.com.cn/gaoceng_developments/index.shtml'  ## 15页
    # 'https://zjnews.zjol.com.cn/gaoceng_developments/yjj/xgsp/'  ## 只有一页
    # 'https://zjnews.zjol.com.cn/gaoceng_developments/zsj/'  ## 只有一页

    ## 所有目录页网址汇总（可选，如果只有一页就不用第二行）
    urls = [url]
    urls += [url.split('index')[0] + 'index_' + str(i) + '.shtml' for i in range(1,3)]

    ## 获取所有文章url
    articles = get_article_url(urls)
    
    if not os.path.exists('../data/'):
        os.makedirs('../data/')

    ## 所有文章url保存(可选)
    save_file = '../data/浙江在线_url.txt'
    save_url(save_file, articles)

    ## 爬取文章内容
    articles = gac.read_url('../data/浙江在线_url.txt')
    batch_size = 10
    batchs = gac.batching(articles, batch_size)
    save_file = '../data/浙江在线_content.txt'
    gac.get_content(articles, batchs, save_file)





