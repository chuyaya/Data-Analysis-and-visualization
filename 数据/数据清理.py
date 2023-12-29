# _*_coding : utf-8 _*_
# @Time : 2022/6/6 15:00
# @Author : chuya
# @File : 爬取数据
# @Project : pacHomework

import pymysql
#连接 MySQL 数据库
connect = pymysql.connect(
host="localhost",
user="root", password="root",
database="pythondata", charset="utf8"
)
def pipei():
    cursor = connect.cursor()  # 获取操作游标
    cursor.execute("select * from jobs")  # 从 jobs 表中查询所有内容并保存
    results = cursor.fetchall()  # 接受全部的返回结果
    after_pipei = []  # 建立一个空列表，用来存储匹配后数据
    for each_result in results:
        if each_result[0] == 'java开发工程师':
            if 'java' in each_result[0] or '开发' in each_result[0]:
                after_pipei.append(each_result)
    cursor.close()  # 关闭游标
    return after_pipei  # 返回匹配后的列

def split_city(data):
    after_split_city = []  #建立一个空列表，用来存储匹配后数据
    for each_date in data:
        each_date_list = list(each_date)
        each_date_list[4] = each_date_list[4].split('-')[0]    #将数据表中工作地点列以'-'进行切割，选取第一个元素替换
        after_split_city.append(each_date_list)
    return after_split_city # 返回筛除后的数据

def salary(data):
    after_salary=[]    #建立一个空列表，用来存储匹配后数据
    for each_data in data:
        each_data=list(each_data)
        if each_data[3] != '' and each_data[3][-1] != '时' and each_data[3][-3] != '下' and each_data[3][-4:-2] != '以下' and each_data[3][-3] != '上':
    # 筛除缺失值，以小时计费，给出的薪资表达为在“……以下”及“……以上”等难以计算数据的工作岗位
    # 统一量纲（单位:千/月）
            if each_data[3][-1] == '年':
                each_data[3] = str(round((float(each_data[3].split('万')[0].split('-')[0]) + float(each_data[3].split('万')[0].split('-')[1])) * 5/12,1)) + '千 / 月'
            elif each_data[3][-1] == '天':
                each_data[3] = str(round((float(each_data[3].split('元')[0]) * 30/1000),1)) +'千 / 月'
            elif each_data[3][-3] == '万':
                each_data[3] = str(round((float(each_data[3].split('万')[0].split('-')[0]) + float(each_data[3].split('万')[0].split('-')[1])) * 5,1)) + '千/月'
            else:
                each_data[3] = str(round((float(each_data[3].split('千')[0].split('-')[0]) + float(each_data[3].split('千')[0].split('-')[1]) /2),1)) + '千 / 月'
        after_salary.append(each_data)
    return after_salary# 返回平均工资后的数据

def job_attribute_text(data):
    for each_data in data:
        if len(each_data[5].split(',')) == 2:
            each_data[5] = ' ' + each_data[5].split(',')[1]

        elif len(each_data[5].split(',')) == 3:
            if ' 经验' in each_data[5].split(',')[1] or ' 在校生' in each_data[5].split(',')[1]:
                each_data[5] = each_data[5].split(',')[1] + ','
                # 以“，”切割后的列表长度为 3，若不包含“经验”元素，则保留“，学历”形式内容
            else:
                each_data[5] = ' ' + each_data[5].split(',')[1] + '-' + each_data[5].split(',')[2]
            # 以“，”切割后的列表长度为 4，选取中间两个元素，保留“经验，学历”形式内容
        elif len(each_data[5].split(',')) == 4:
            each_data[5] = each_data[5].split(',')[1] + ',' + each_data[5].split(',')[2]
    return data

#将清洗后的数据保存到数据库中 after_clean 表中，代码和保存爬取数据时类似
def save(data):
    cursor = connect.cursor()
    for each_data in data:
        present_job = each_data[0]
        job_name = each_data[1]
        company_name = each_data[2]
        providesalary_text = each_data[3]
        workarea_text = each_data[4]
        jobwelf = each_data[5]
        sql = "insert into after_clean(present,job_name,company,salary,area,job_Requirements) values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[present_job, job_name,company_name,providesalary_text,workarea_text, jobwelf])
        connect.commit()
    cursor.close()
    connect.close()
# 2.2进行数据清洗
if __name__ == "__main__":
    data = pipei()
    data1 = split_city(data)
    data2 = salary(data1)
    data3 = job_attribute_text(data2)
    save(data2)
