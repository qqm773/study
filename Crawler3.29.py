# -*- codeing = utf-8 -*-
# @Time : 2021/3/29 9:31
# @Author : 疏苑
# @File : Crawler3.29.py
# @Software : PyCharm

# -*- codeing = utf-8 -*-
# @Time : 2021/3/28 16:02
# @Author : 疏苑
# @File : crawler3.28.py
# @Software : PyCharm
import os
import re  # 正则表达式，文字匹配用
from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request  # 制定URL，获取网页数据
import urllib.error
import requests
import xlwt  # Excel操作用
import time


def main():
    baseurl = "https://www.dushu.com/book/1255_"
    datalist = getData(baseurl)
    # askURL("https://www.dushu.com/search.aspx?wd=%e8%a5%bf%e6%96%b9%e6%88%98%e4%ba%89&p=")
    savepath = "图书表_关键词_西方战争_来源_读书网.xls"
    saveDate(datalist, savepath)



keyword = '军事理论'
# findNumber = re.compile('<strong class="text-dot">(\d+)</strong>')  # 匹配搜索结果数
findBookId = re.compile('<h3><a href="(.*?)"')  # 匹配图书编号
findTitle = re.compile('<h1>(.*?)</h1>')  # 匹配书名
findAbstract = re.compile(r'<div class="text txtsummary">(.*?)</div>', re.S)  # 匹配摘要
findPic = re.compile('<div class="pic"><img alt=.* src="(.*?)".*</div>')
Number = 0
bookurl = "https://www.dushu.com"
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    'Referer': 'https://www.dushu.com/search.aspx?wd=%e8%a5%bf%e6%96%b9%e6%88%98%e4%ba%89&p=2'
}


# 2.分析数据
def getData(baseurl):
    count = 0
    pic_path = "./" + keyword  # 创建存放图片的文件夹
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)

    datalist = []
    # baseaskURL(baseurl)
    # page = Number // 20 + 1
    # print(page)
    for i in range(0, 10):
        url = baseurl + str(i + 1) + '.html'
        html = askURL(url)

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="book-info"):  # 查找符合要求的字符串，形成列表
            data = []  # 将查找的图书概括存储
            item = str(item)
            bookid = re.findall(findBookId, item)
            bookid = str(bookid)
            bookid = re.sub("[\'\[\]]", '', bookid)
            burl = bookurl + bookid
            # print(burl)
            bookhtml = askURL(burl)
            bs = BeautifulSoup(bookhtml, 'html.parser')

            # 标题信息
            title = re.findall(findTitle, bookhtml)[0]
            print(title)
            count += 1
            print(count)
            data.append(title)

            # 属性（作者，出版社，出版日期）
            total = bs.select("table>tbody>tr>td~td")
            author = str(total[0])
            author = re.sub("[<>td/著编]", "", author)
            # print(author)
            data.append(author)

            publish_house = str(total[1])
            publish_date = str(total[6])
            publish_house = re.sub("[<>td/]", "", publish_house)
            publish_date = re.sub("[<>td/clas=\"r]", "", publish_date)
            publish_date = re.sub('-', '/', publish_date)
            # print(publish_house)
            # print(publish_date)
            data.append(publish_house)
            data.append(publish_date)

            # 摘要
            abstract = re.findall(findAbstract, bookhtml)[0]
            # print(abstract)
            data.append(abstract)

            # 封面

            pic = bs.select('[class="pic"]')
            pic = re.findall(findPic, str(pic))
            pic = str(pic)
            pic = re.sub("[\[\]\']", '', pic)
            # print(pic)
            pic_name = title + '.jpg'

            res = requests.get(pic, headers=head)
            time.sleep(0.5)
            with open(pic_path + '/' + pic_name, 'wb') as f:
                if res.status_code == 200:
                    try:
                        f.write(res.content)
                        data.append(pic_path + '/' + pic_name)
                    except (FileNotFoundError, FileExistsError):
                        print("第%d本书-%s" % (count, title))
                        continue
                else:
                    print('%s''异常' % title)
            # print(pic)
            datalist.append(data)
            # print(datalist)
            # break
    # print(datalist)

    return datalist

    # print(abstract)
    # print(bookhtml)

    # break

    # print(item)


# 1.爬取网页
def baseaskURL(url):
    # head = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    # }
    # head = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
    # }
    req = urllib.request.Request(url, headers=head)
    html = ""

    try:
        resp = urllib.request.urlopen(req)
        html = resp.read().decode("utf-8")
        # print(html)
        # global Number
        # Number = int(re.findall(findNumber, html)[0])
        # print(Number)
        # print(type(Number))
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


def askURL(url):
    req = urllib.request.Request(url, headers=head)
    html = ""

    try:
        resp = urllib.request.urlopen(req)
        html = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 3.保存数据为excel文件
def saveDate(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet(keyword, cell_overwrite_ok=True)
    col = (' ', "title", "author", "publish_house", "publish_date", "_abtract", "image_url")
    for i in range(0, 7):
        worksheet.write(0, i, col[i])
    for i in range(0, 400):
        print("第%d条" % (i + 1))
        data = datalist[i]
        worksheet.write(i + 1, 0, i + 1)
        for j in range(0, 6):
            worksheet.write(i + 1, j + 1, data[j])

    workbook.save(savepath)

    print("save")


if __name__ == '__main__':
    main()
