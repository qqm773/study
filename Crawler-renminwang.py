# -*- codeing = utf-8 -*-
# @Time : 2021/4/1 20:23
# @Author : 疏苑
# @File : gaochengbaodao.py
# @Software : PyCharm

import os
import re  # 正则表达式，文字匹配用
from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request  # 制定URL，获取网页数据
import urllib.error
import requests  # 图片获取
import xlwt  # Excel操作用
import time


# 人民网军事

def main():
    # baseurl = "http://military.people.com.cn/GB/52963/index.html"
    for i in range(0,8):
        datalist = getData(baseurl[i])
        savepath = "2021年4月8日媒体文章表_分类_"+keyword[i]+"_来源_人民网军事.xls"
        saveDate(datalist, savepath)
        time.sleep(100)
        global jk
        jk += 1

jk = 0
baseurl = ["http://military.people.com.cn/GB/172467/index","http://military.people.com.cn/GB/52963/index","http://military.people.com.cn/GB/115150/index","http://military.people.com.cn/GB/52936/index","http://military.people.com.cn/GB/367527/index","http://military.people.com.cn/GB/1077/index","http://military.people.com.cn/GB/42969/index","http://military.people.com.cn/GB/367540/index"]
pas = set()
keyword = ['滚动新闻','高层动态','国防部','本网原创','中国军情','国际军情','评论','名家论剑']
findNewurl = re.compile('<a href="(.*?)"')  # 匹配新闻链接尾部
findTitle = re.compile('<h1>(.*?)</h1>')  # 匹配书名
findAuthor = re.compile(r'<div class="edit cf">(.*?)</div>')  # 匹配作者
# findSource = re.compile('<meta name="source"(.*?)">')  # 匹配来源
# findContect = re.compile('<p style="text-indent: 2em;">')
# findPic = re.compile('<div class="pic"><img alt=.* src="(.*?)".*</div>')
findPage = re.compile('PageNo=(.+)', re.S)
Number = 0
# baseurl = "http://military.people.com.cn"
head = [{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    'Referer': 'http://military.people.com.cn/GB/172467/index.html'
},{
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Referer': 'http://military.people.com.cn/GB/52963/index.html'
},{
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    'Referer': 'http://military.people.com.cn/GB/115150/index.html'
},{
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    'Referer': 'http://military.people.com.cn/GB/52936/index.html'
},{
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0",
    'Referer': 'http://military.people.com.cn/GB/367527/index.html'
},{
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    'Referer': 'http://military.people.com.cn/GB/1077/index.html'
},{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    'Referer': 'http://military.people.com.cn/GB/42969/index.html'
},{
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    'Referer': 'http://military.people.com.cn/GB/367540/index.html'
},]


# 2.分析数据
def getData(baseurl):
    count = 0
    global jk
    # pic_path = "./" + keyword  # 创建存放图片的文件夹
    # if not os.path.exists(pic_path):
    #     os.mkdir(pic_path)
    datalist = []
    html = askURL(baseurl + '.html')
    # print(html)

    bs = BeautifulSoup(html, "html.parser")
    page = bs.find(text=findPage)
    page = int(re.sub('\D', '', page))
    for i in range(0, page):
        url = baseurl + str(i + 1) + '.html'
        html = askURL(url)

        bs = BeautifulSoup(html, "html.parser")
        newlist = bs.find_all(class_="list_16 mt10")
        newlist = str(newlist)
        newlist = re.findall(findNewurl, newlist)  # 获得每页的新闻链接
        # print(type(newlist))


        # 2.逐一解析数据
        for item in newlist:  # 查找符合要求的字符串，形成列表
            if item in pas:
                continue
            pas.add(item)
            data = []
            item = str(item)
            newurl = baseurl + item
            # print(newurl)
            html = askURL(newurl)
            request = requests.get(newurl)
            httpStatusCode = request.status_code
            if httpStatusCode!=200:
                continue
            # print(html)
            bs = BeautifulSoup(html, "html.parser")
            title = re.findall(findTitle, html)[-1] # 标题
            title= re.sub('&nbsp;','',title)


            data.append(title)

            author = re.findall(findAuthor, html)  # 责编
            author = str(author)
            author = re.sub('[\[\]()\'责编：]', '', author)
            data.append(author)
            # print(author)

            source = bs.find(attrs={"name":"source"})['content']
            source=re.sub('[来源：]', '', source)
            # print(source)
            data.append(source)

            publis_date = bs.find(attrs={"name":"publishdate"})['content']
            publis_date = re.sub('[-]','/',publis_date)
            if publis_date<='2021/04/02':
                continue
            data.append(publis_date)
            # print(publis_date)
            print(title)
            contect = bs.select('[style="text-indent: 2em;"]')
            if contect == []:
                continue
            contect = str(contect)
            contect = re.sub('<p style="text-indent: 2em;">','',contect)
            contect = re.sub('</p>','',contect)
            contect = re.sub('[,\[\]]','',contect)
            # print(contect)
            print(title)
            count += 1
            print(count)
            data.append(contect)


            data.append(keyword[jk])
            # print(len(data))
            # print(data)
            datalist.append(data)

    return datalist


# 1.爬取网页

def askURL(url):
    req = urllib.request.Request(url, headers=head[jk])
    html = ""

    try:
        resp = urllib.request.urlopen(req,timeout=10)
        html = resp.read().decode("GBK")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 3.保存数据为excel文件
def saveDate(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    global jk
    worksheet = workbook.add_sheet(keyword[jk], cell_overwrite_ok=True)
    col = (' ', "title", "author", "source", "publish_date", "content","tag")
    for i in range(0, 7):
        worksheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        if datalist[i]:
            # print("第%d条" % (i + 1))
            data = datalist[i]
            worksheet.write(i + 1, 0, i + 1)
            for j in range(0, 6):
                worksheet.write(i + 1, j + 1, data[j])
        else:
            break

    workbook.save(savepath)

    print(str(jk)+"save")


if __name__ == '__main__':
    main()
