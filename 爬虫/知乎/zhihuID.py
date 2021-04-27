## 使用方法：
## 先选择需要爬取的知乎话题，找到该话题对应的id，赋值给topic_id。例：https://www.zhihu.com/topic/19652943/hot
## 选择文章中和标题中是否都需要出现关键词
##


import requests
import re
import zhihuanswerdowload

class ZhiHuCrawler(object):
    def __init__(self):
        """
        headers         请求头信息
        end_offset      话题下精华问题的最大数目（最大偏移量）
        end_offset2     问题下回答的最大数目（最大偏移量）
        pattern         匹配所有html标签
        patten2         匹配超链接
        comments        爬取的问题的所有评论（格式：[['question_title', 'answer']]）
        q_num           爬取的精华问题的个数
        ans_num         爬取的回答的问题个数
        """
        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        self.pattern = re.compile(r'<[^>]*>')
        self.pattern2 = re.compile(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
        self.comments = []
        self.q_num = 10
        self.ans_num = 4

    def crawl(self, topic_id, keyword, num=0):
        prev = []  # 判断当前问题和之前问题是否重复
        i = 0
        question_num = self.q_num
        while i < question_num:
            json_url = 'https://www.zhihu.com/api/v4/topics/' + str(
                topic_id) + '/feeds/essence?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F' \
                            '(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3D' \
                            'topic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author' \
                            '.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.c' \
                            'ontent%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.' \
                            'target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)' \
                            '%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(ta' \
                            'rget.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B%' \
                            '3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Cco' \
                            'mment_count&offset=' + str(i) + '&limit=' + str(question_num + 10)

            response = requests.get(url=json_url, headers=self.headers, timeout=5)
            exit() if response.status_code != requests.codes.ok else print('Request question Successfully')
            response_json_dict = response.json()
            resp_quesion_data = response_json_dict['data']

            # 判断页面是否到头
            # 这是另一种办法: if response_json_dict.get('paging').get('is_end') is False:

            for j in range(len(resp_quesion_data)):
                if resp_quesion_data[j] != []:
                    api_url = resp_quesion_data[j].get('target').get('question').get('url')
                    title = resp_quesion_data[j].get('target').get('question').get('title')  ## 标题中是否需要包含关键词
                    question_id = resp_quesion_data[j].get('target').get('question').get('id')

                    if api_url not in prev:
                        if keyword in title:  ## 含有关键词的问题
                            print(title)
                            zhihuanswerdowload.GetAnswer(question_id, keyword=keyword, num=num)
                            prev.append(api_url)
                        else:
                            print('{}不包含关键词{}'.format(title, keyword))
                else:
                    continue
            i = i + 1

if __name__ == '__main__':
    xupt_topic_id = 19565565  ## 知乎的话题id
    xupt_topic_id_ai = 19551275
    xupt_topic_id_zidongjiashi = 19635352
    # keyword = '自动驾驶'
    keyword = ''  ## 只能支持一个关键词，也可以没有
    crawler = ZhiHuCrawler()
    crawler.crawl(topic_id=xupt_topic_id_zidongjiashi, keyword=keyword, num=6)
