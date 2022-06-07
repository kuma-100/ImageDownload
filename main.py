# -*- coding:utf-8 -*-
import re
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path  # 关于文件路径操作的库，这里主要为了得到图片后缀名
from openpyxl import load_workbook


def down_html(url):
    # url = 'https://natalie.mu/music/gallery/news/408303/1499999'
    result = requests.get(url, headers=headers)
    print(url)
    fp = open('html.txt', 'wb')
    fp.write(result.content)
    fp.close()


def dowmload_pic(html, word, regex):
    pic_url = re.findall(regex, html, re.S)
    i = 1
    print('找到关键词:' + word + '的图片，现在开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            continue
        # 设置Path变量，为了使用Pahtlib库中的方法提取后缀名
        p = Path(each)
        # 得到后缀，返回的是如 '.jpg'
        p_suffix = p.suffix
        dir = './images/' + word + '_' + str(i) + p_suffix
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1


def baidu():
    word = input("请输入百度搜图名: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    down_html(url)
    # result = requests.get(url, headers=headers)
    # regex = '"objURL":"(.*?)",'
    # dowmload_pic(result.text, word, regex)


def other():
    word = input("请输入图片名: ")
    url = 'https://natalie.mu/music/gallery/news/408303/1499999'
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    soup_result = soup.select(".GAE_galleryListImage img").__str__()
    regex = 'data-src="(.*?)\?'
    # pic_url = re.findall(regex, soup_result, re.S)
    # print(pic_url)
    dowmload_pic(soup_result, word, regex)


def bilibili():
    word = input("请输入b站用户名: ")
    num = 1
    url = 'https://search.bilibili.com/upuser?keyword=' + word + '&page=' + str(num)
    result = requests.get(url, headers=headers)
    regex = '"objURL":"(.*?)",'
    down_html(url)

def SevenEleven():
    # １指定ajax-post请求的url（通过抓包进行获取）
    url = 'https://www.7-11.cn/ajax/ajax.aspx'

    # 处理post请求携带的参数(从抓包工具中获取)
    data = {
        'act': 'ShopScreening',
        'AreaID': '520',
    }

    # 自定义请求头信息，相关的头信息必须封装在字典结构中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }

    # 2.发起基于ajax的post请求
    response = requests.post(url=url, data=data, headers=headers)

    # 获取响应内容：响应内容为json串
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    # print(soup)
    td4_all=[]
    td5_all=[]
    for td4 in soup.select('td.weizhi-4'):
        # print('String:', td4.string)
        td4_all.append(td4.string)
    for td5 in soup.select('td.weizhi-5'):
        # print('get text:', td5.get_text())
        td5_all.append(td5.string)
    #写入Excel
    workbook = load_workbook(filename='list1.xlsx')
    sheet = workbook.active
    A = 0
    for td in td4_all:
        A += 1
        str1 = 'A' + str(A)
        sheet[str1].value = td4_all[A-1]
        # print(td4_all[A-1])
    B = 0
    for td in td5_all:
        B += 1
        str2 = 'B' + str(B)
        sheet[str2].value = td5_all[B-1]
        # print(td5_all[B-1])
    print('正在读取的页面：' + url)
    workbook.save(filename='list1.xlsx')

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57'}
    # down_html()
    # baidu()
    # other()
    # bilibili()
    SevenEleven()