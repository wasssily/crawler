# crawler

多个平台的爬虫代码整理

浙江在线：crawler.py, get_article_content.py 
crawler.py 为主程序，其中调用get_article_content.py，也可直接使用get_article_content.py，但前提是已经获取了所有文章的单链。

知乎： zhihuID.py, zhihuanswerdownload.py
zhihuID.py可以爬取单一话题下的所有相关问题，其中调取zhihuanswerdownload.py，对单个问题下的所有回答进行爬取。

学习强国： 有点问题，只能爬部分 且要对网址做如下形式的修改: url_origin >>> url

url = 'https://www.xuexi.cn/588a4707f9db9606d832e51bfb3cea3b/data9a3668c13f6e303932b5e0e100fc248b.js'

url_origin = 'https://www.xuexi.cn/588a4707f9db9606d832e51bfb3cea3b/9a3668c13f6e303932b5e0e100fc248b.html'

即，最后一个/后面要加上data，且后缀要改成.js
