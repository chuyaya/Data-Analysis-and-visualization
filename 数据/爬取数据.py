# _*_coding : utf-8 _*_
# @Time : 2022/6/6 15:00
# @Author : chuya
# @File : 爬取数据
# @Project : pacHomework

from bs4 import BeautifulSoup
import pymysql
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time

# 1.2对每个岗位搜索的到的总页数进行爬取
if    __name__     == '__main__': #主函数
    job=["java开发工程师","Web前端","嵌入式"]
    option = ChromeOptions()    #启动chrome选项
    # User - Agent反爬虫, 这是一个请求头信息, 是请求载体的身份标识
    UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 Edg/94.0.992.31"
    option.add_argument(f'user-agent={UA}')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    web = webdriver.Chrome(options=option)
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    web.implicitly_wait(3)
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,Java%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?'

    web.get(url)
    #全屏最大化浏览器
    web.maximize_window()

    time.sleep(6)
    page_list=[]
    for j in job:
        for i in range(1, 1 + 1):
            url="https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?".format(j, i)
            web.get(url)
            html = web.page_source
            page = BeautifulSoup(html, "lxml")
            text = page.find_all("script", type="text/javascript")[3].string
            page_te = eval(str(text).split("=", 1)[1])["total_page"]
            page_list.append(page_te)
            print(page_te)

#定义 jiexi()函数，用于解析得到的 html
def jiexi(html, info,name):
    page = BeautifulSoup(html, "lxml")
    text = page.find_all("script", type="text/javascript")[3].string
    #观察原始代码发现我们需要的数据在 engine_jds 后
    data = eval(str(text).split("=", 1)[1])["engine_jds"]
    for d in data:
        try:
            job_name = d["job_name"].replace("\\", "") # 岗位名称
        except:
            job_name = " "
        try:
            company_name = d["company_name"].replace("\\", "")  # 公司名称
        except:
            company_name = " "
        try:
            providesalary_text = d["providesalary_text"].replace("\\", "")  # 薪资
        except:
            providesalary_text = " "
        try:
            workarea_text = d["workarea_text"].replace("\\", "")   #工作地点
        except:
            workarea_text = " "
        try:
            at = d["attribute_text"]  # 工作要求
            s = ''
            for i in range(0, len(at)):
                s = s + at[i] + ','
                attribute_text = s[:-1]
        except:
            attribute_text = " "
        info.append( [ name,job_name, company_name, providesalary_text,workarea_text,attribute_text])

def save(info):
    for data in info:
        present_job = data[0]            # 当前爬取岗位
        job_name = data[1]                #岗位
        company_name = data[2]      #公司名称
        providesalary_text = data[3]  #薪资
        workarea_text = data[4]         #工作地点
        jobwelf = data[5]                    #工作待遇
        # 创建 sql 语句
        sql = "insert into jobs(present_job,job_name,company,salary,area,job_Requirements) values(%s,%s,%s,%s,%s,%s)"
        # 执行 sql 语句
        cursor.execute(sql, [present_job, job_name,company_name, providesalary_text,workarea_text, jobwelf])
        connect.commit()  # 提交保存到数据库



# 1.4进行数据的爬取
if    __name__     == '__main__':
    job=["java开发工程师","Web前端","嵌入式"]
    page_list=['100','2','2']
    option = ChromeOptions()
    UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 Edg/94.0.992.31"
    option.add_argument(f'user-agent={UA}')
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    web = webdriver.Chrome(options=option)
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    web.implicitly_wait(10)
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,Java%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?'
    web.get(url)
    time.sleep(6)
    le=len(job)
    connect = pymysql.connect(  # 连接数据库
        host="localhost",
        user="root",  # 用户名
        password="root",  # 密码
        database="pythondata",  # 操作的数据库名称charset="utf8"
    )
    #创造游标
    cursor = connect.cursor()
    for j in range(0,le):
        for i in range(1,int(page_list[j])):#页面
            info = []
            url = "https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?".format(job[j], i)
            web.get(url)
            ht = web.page_source
            page = BeautifulSoup(ht, "lxml")
            jiexi(ht, info,job[j])     #调用解析函数
            print('岗位{}:{}/{}'.format(j,i,page_list[j]))
            time.sleep(2)
            save(info)                 #调用保存函数
        time.sleep(3)
    cursor.close()
    connect.close()











    # def spider(url):
    #     headers = {
    #         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31"}
    #     try:
    #         rep = requests.get(url, headers=headers)
    #         rep.raise_for_status()
    #         rep.encoding = rep.apparent_encoding
    #         txt = rep.text
    #         return txt
    #     except:
    #         print("解析失败")
