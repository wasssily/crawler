#!/user/bin/python
# -*-coding:utf-8-*-
# author：luoxiaoxu
# blog:xiaoxu.online
# Filename: ZhihuAnswerDowload.py
# Function: 根据知乎问题的编号（https://www.zhihu.com/question/453859882（最后这个编号））爬取知乎问题中含有特定关键词的回答

import requests
import os
import re
import csv
import json

def GetAnswer(Question_ID, keyword, num, save_path):
    Question_ID = Question_ID
    keyword = keyword
    keywords = keyword.split()
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                             " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    limit = 5  # 每次显示的答案个数
    offset = 0  # 下一次显示的回答偏移量
    browse_num = 0  # 已经遍历的回答个数
    record_num = 0  # 含关键字的回答个数
    title = ''
    if not os.path.exists('../知乎下载/'):
        os.makedirs('../知乎下载/')
    print('\n正在爬取……\n')

    url = "https://www.zhihu.com/api/v4/questions/{Question_ID}/answers?include=content&limit=" \
          "{limit}&offset={offset}&platform=desktop&sort_by=default" \
        .format(Question_ID=str(Question_ID), limit=str(limit), offset=str(offset))
    res = requests.get(url, headers=headers)
    try:
        res = json.loads(res.content)
    except:
        print('问题编号输入错误！\n')
        return None
    total_num = res['paging']['totals']  ##该问题下的回答数量
    if num != 0:
        total_num = num
    cons = res['data']
    while browse_num < total_num:  ## 设置爬取的回答数量
        if cons is not None:
            if total_num <= 0:
                print('该问题暂时无答案！')
                break
            if title == '':
                title = cons[0]['question']['title']
                path_txt = CreativeFile(title, keyword, save_path)
            for con in cons:
                browse_num += 1
                Re = re.compile(r'<[^>]+>', re.S)
                answer_detail = Re.sub('', con['content'])  # 获取具体回答内容
                flag = True
                if len(keywords) > 0:
                    flag = HasKeywords(answer_detail, keyword)  # 查询是否有关键词
                if flag:
                    record_num += 1
                    answer_txt = []
                    answer_txt.append('\n' + answer_detail)  ## + \
                                      # '\n-------------------------------------------------------------------------------\n')
                    Save2File_txt(path_txt, answer_txt)
                    print('已保存第%d个回答\n' % record_num)

            offset += len(cons)
            if len(cons) < limit:  # 已爬取到最后一页
                break
    if len(keywords) == 0:
        print('爬取完成，已保存所有%d个回答！\n' % record_num)
    elif record_num > 0:
        print('爬取完成，已保存%d个与关键词有关的回答！\n' % record_num)
    else:
        os.remove(path_txt)
        print('未找到与关键词有关的答案\n')


def Save2File_csv(path, content):
    f = open(path, 'a+')
    writer = csv.writer(f)
    writer.writerow(content)
    f.close()


def Save2File_txt(path, contents):
    f = open(path, 'a+', encoding='utf-8')
    for content in contents:
        f.writelines(content)
    f.writelines('\n')
    f.close()


def HasKeywords(answer_detail, keyword):  # 判断是否含有全部关键词
    flag = True
    for key in keyword.split():
        flag2 = False
        for sub_key in key.split('+'):
            flag2 = flag2 or answer_detail.find(sub_key) > 0
            if flag2:
                break
        flag = flag and flag2
        if not flag:
            return False
    return True

def CreativeFile(title, keyword, save_path):
    path_txt = save_path + title + '.txt'
    if os.path.exists(path_txt):
        f = open(path_txt, 'w')
        f.seek(0)
        f.truncate()
        f.close()
    Save2File_txt(path_txt, [title, '关键字：' + keyword + '\n'])
    return path_txt

if __name__ == '__main__':
    Question_ID = '380314348'  ## 问题id
    keyword = '5G 信号'  ## 多个关键词用空格隔开
    num = 0  ## 问题数量限制,若没有限制，则取0
    save_path = '../知乎下载/'
    GetAnswer(Question_ID, keyword, num, save_path)
