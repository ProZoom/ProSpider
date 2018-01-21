#!/usr/bin/env python
# coding: utf-8

import itertools
import urllib
import re
from multiprocessing import Pool
from Utils.baseUtils import *
from SpiderForPics.SpiderForPicsConfig import *


# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = URL
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')


def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


# 开始
def start(name, dir):
    # 搜索关键字
    word = name
    # 创建目录
    dirpath = mkDir(dir)
    # 将关键字整合到url中
    urls = buildUrls(word)
    # 次数
    index = 0

    for url in urls:
        print("<---正在请求--->：", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print(name, ": 已下载 %s 张" % index)
                if index == numIMGS:
                    return


if __name__ == '__main__':
    # 相对路径
    BASE = 'res'
    print("欢迎使用百度图片下载爬虫<多类别搜索>")
    print("   ➤ 抓包的默认路径为相对目录imgs！")
    pic_types = input("请输入你要下载的图片类别词<多个类别词请用空格>：\n")
    xlist = pic_types.split(' ')

    PIC_TYPES = dict(zip(xlist, xlist))
    print(PIC_TYPES)
    print("➸ " + "♔" * 50 + " ☚")
    numIMGS = input('请输入您要下载图片的数量:')
    if numIMGS != '':
        numIMGS = int(numIMGS)
    else:
        numIMGS = 10
    print("➸ " + "♔" * 50 + " ☚")

    # 进程池
    POOLNUM = 4
    p = Pool(processes=POOLNUM)

    for name, dir in PIC_TYPES.items():
        dir = os.path.join(BASE, dir)
        print(name, dir)
        p.apply_async(start, (name, dir))

    print('❂ 等待抓包完成')

    p.close()
    p.join()
    print('✓ 抓包完成！')
