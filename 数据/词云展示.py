# _*_coding : utf-8 _*_
# @Time : 2022/6/6 15:00
# @Author : chuya
# @File : 爬取数据
# @Project : pacHomework
import wordcloud
import numpy as np
from PIL import Image  # Image模块是在Python PIL图像处理常用的模块
import jieba

pic = Image.open("a.png")  # 打开图片路径，形成轮廓
shape = np.array(pic)  # 图像轮廓转换为数组
wc = wordcloud.WordCloud(mask=shape, font_path="simkai.ttf", background_color="white",
                         max_font_size=100)  # mask为图片背景，font_path为字体，若不设置可能乱码

text = open(r'after_clean.txt', "r", encoding='UTF-8').read()  # 对中文应该设置编码方式为utf—8
cut_text = jieba.cut(text)
result = " ".join(cut_text)
wc.generate(result)
wc.to_file("cloud.jpg")


# import jieba
# from wordcloud import WordCloud
# from wordcloud import WordCloud
# import PIL.Image as image
# import numpy as np
# import jieba
# import xlrd
#
#
# def trans_CN(text):
#     word_list = jieba.cut(text)  # 分词后在单独个体之间加上空格
#     result = " ".join(word_list)
#     return result;
#
#
# if __name__ == "__main__":
#     '''
#     此代码是为了生成点云：
#     1.需要爬虫得到的xls数据，这个在之前已经完成。
#     2.需要运行toText.py 读取xls对应列数据 生成txt
#     3.运行此代码 将生成的txt读入 生成词云
#
#     '''
#
#     # 此处job.txt 需与xls转化生成的txt名字对应
#     with open("after_clean.txt", encoding='utf-8') as fp:
#         text = fp.read()
#         text = trans_CN(text)  # print(text)
#         mask = np.array(image.open("a.png"))
#         wordcloud = WordCloud(
#             mask=mask,
#             font_path="msyh.ttc"
#         ).generate(text)
#         image_produce = wordcloud.to_image()
#         image_produce.show()



