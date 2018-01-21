# coding:utf-8
import requests
import re
import itertools
import urllib
from Utils.baseUtils import *
from SpiderForPics.SpiderForPicsConfig import *


# 解码
def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url.translate(char_table)


def buildUrls(word):
    word = urllib.parse.quote(word)
    url = URL
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


re_url = re.compile(r'"objURL":"(.*?)"')


# 获取imgURL
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


if __name__ == '__main__':

    print("欢迎使用百度图片下载爬虫<多个关键字搜索>")
    # choosePath = input('请输入你想保存的路径方式\n  1. 默认路径 path = imgs/ \n  2. 相对路径 path_input/path_input/ \n  3. 绝对路径,比如 D:/img/\n')
    # if int(choosePath) == 3:
    #     dirpath = input('请输入您要保存图片的路径\n')
    # elif int(choosePath) == 2:
    #     path = input('请输入您要保存图片的路径\n')
    #     dirpath = mkDir(path)
    # else:
    #     path = 'imgs'
    #     dirpath = mkDir(path)
    print("   ➤ 抓包的默认路径为相对目录imgs！")
    path = 'imgs'
    dirpath = mkDir(path)

    print("➸ " + "♔" * 50 + " ☚")
    word = input("请输入你要下载的图片关键词<多个关键字请用空格进行分割>：\n")
    print("➸ " + "♔" * 50 + " ☚")

    chooseImgType = input('请选择你要保存的图片格式\n  0. default: jpg \n  1. jpg\n  2. png\n  3. gif\n  4. 自定义\n')
    chooseImgType = int(chooseImgType)
    if chooseImgType == 4:
        imgType = input('请输入自定义图片类型\n')
    elif chooseImgType == 1:
        imgType = 'jpg'
    elif chooseImgType == 2:
        imgType = 'png'
    elif chooseImgType == 3:
        imgType = 'gif'
    else:
        imgType = 'jpg'
    print("➸ " + "♔" * 50 + " ☚")

    strtag = input("请输入您要下载图片名字,最后格式为 number+' '+name.%s\n" % imgType)

    print("➸ " + "♔" * 50 + " ☚")
    numIMGS = input('请输入您要下载图片的数量\n')
    numIMGS = int(numIMGS)

    urls = buildUrls(word)
    index = 0
    print("➸ " + "♔" * 50 + " ☚")
    for url in urls:
        print("正在请求：", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        # print(imgUrls)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImgWithFormat(url, dirpath, str(index + 1) + ' ' + strtag, imgType):
                index += 1
                print("已下载 %s 张" % index)
                # 双 break 跳出下载循环
            if index == numIMGS:
                break
        if index == numIMGS:
            print('您一共下载了 %s 张图片' % index)
            print('程序正在终止')
            break
