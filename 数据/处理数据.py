# _*_coding : utf-8 _*_
# @Time : 2022/6/6 15:00
# @Author : chuya
# @File : 爬取数据
# @Project : pacHomework

# 3.7 岗位工作待遇热词词云图
#设计词频统计函数
import jieba
import pymysql


def wordcount(txt):
    #转化为列表
        # 统计词频的字典
    word_freq = dict()
    # 装载停用词,此处需将资料中给出的hit_jobs.txt 文件放到本代码所在路径下
    with open(r"L:\coursemyself\venv\myself\爬虫大作业代码\数据\jobs.txt", "r", encoding='utf-8') as f1:
        # 读取我们的待处理本文
        txt1 = f1.readlines()
    stoplist = []
    for line in txt1:
        stoplist.append(line.strip('\n'))

    #  切分、停用词过滤、统计词频
    for w in list(jieba.cut(txt)):
        if len(w) > 1 and w not in stoplist:
            if w not in word_freq:
                word_freq[w] = 1
            else:
                word_freq[w] = word_freq[w] + 1
    return word_freq

import pandas as pd
#连接数据库
db = pymysql.connect(
    host="localhost",
    user="root", password="root",
    database="pythondata", charset="utf8"
)
cursor = db.cursor()
cursor.execute("SELECT `area` FROM `jobs`")
results = cursor.fetchall()
txt = ''
for each_result in results:
    txt = txt + each_result[0]
word_dict=wordcount(txt)
da = pd.DataFrame({'word': word_dict.keys(), 'count': word_dict.values()})
#将词频统计的结果导出
da.to_csv(r'L:\coursemyself\venv\myself\爬虫大作业代码\数据\word_count.csv')
#将导出的词频文件导入到tableau进行词云图的绘制




