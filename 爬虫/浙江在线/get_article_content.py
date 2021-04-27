# -*-coding:utf-8 -*-

"""
# File       : get_article_content.py
# Time       ：2021/4/23 20:58
# Author     ：wassily
# version    ：python 3.7
# Description：
"""

import re
from bs4 import BeautifulSoup
import urllib.request as ur

## 读取文章url
def read_url(url_file):
    file=open(url_file,'r')
    content=[list(eval(i))for i in file]
    file.close()
    articles={}
    for i in content:
        articles[i[0]]=i[1]
    print('总共有{}篇文章需要爬取'.format(len(articles)))
    return articles

def batching(articles, batch_size):
    article_num = len(articles)
    batchs = [batch_size for i in range(article_num//batch_size)]
    batchs.append(article_num % batch_size)
    print('共分成{}批次进行爬取'.format(len(batchs)))
    return batchs


def get_content(articles, batchs, save_file):
    num = 0
    batch_s = 0
    for batch in batchs:
        contents = []
        for i in range(batch):
            article_url = list(articles.values())[num]
            try:
                res = ur.urlopen(article_url)
                soup = BeautifulSoup(res, "html5lib")
                for j in soup.find_all('div', class_='contTxt contTxtFix'):
                # for j in soup.find_all('div', class_='contTxt'):  ##xjp
                    con = j.findAll('p')
                    cont = [str(i.get_text) + '\n' for i in con]
                    pattern1 = r'[a-zA-Z<>\."\_\-=:;\u3000/\s]*'
                    content1 = [re.sub(pattern1, '', i) for i in cont]
                    pattern2 = r'\d{4,100}'  ## 部分页面有图片，爬下来之后是一长串数字，在此进行剔除
                    content2 = [re.sub(pattern2, '', i) for i in content1]
                    content3 = [i.replace('楷体,', '').replace('楷体2312,','') for i in content2]
                    contents += content3
                print('第{}篇文章爬取成功'.format(num+1))
            except:
                print(list(articles.keys())[num],'爬取失败')
                pass
            num += 1
        with open(save_file, 'a+', encoding='utf-8') as f:
            for c in contents:
                f.write(c)
                f.write('\n')
        batch_s += 1
        print('第{}个批次爬取结束'.format(batch_s))

if __name__ == '__main__':
    articles = read_url('../data/浙江在线_url.txt')
    batch_size = 10
    batchs = batching(articles, batch_size)
    if not os.path.exists('../data/浙江在线/'):
        os.makedirs('../data/浙江在线/')
    save_file = '../data/浙江在线/浙江在线_content.txt'
    get_content(articles, batchs, save_file)