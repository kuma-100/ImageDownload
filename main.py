# -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup


def down_html():
    url = 'https://natalie.mu/music/gallery/news/408303/1499999'
    result = requests.get(url, headers=headers)
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

        dir = './images/' + word + '_' + str(i) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1


def baidu():
    word = input("请输入百度搜图名: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    result = requests.get(url, headers=headers)
    regex = '"objURL":"(.*?)",'
    dowmload_pic(result.text, word, regex)


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


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57'}
    # down_html()
    # baidu()
    other()
