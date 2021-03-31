# -*- codeing = utf-8 -*-
# @Time : 2021/3/31 7:51
# @Author : 疏苑
# @File : Crawler3.31.py
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
    baseurl = "http://military.people.com.cn/GB/172467/index"
    datalist = getData(baseurl)
    # savepath = "媒体文章表_分类_"+keyword+"_来源_光明网军事.xls"
    # saveDate(datalist, savepath)



keyword = '滚动新闻'
findNewurl =re.compile('<a href="(.*?)"') #匹配新闻链接尾部
findTitle = re.compile('<h1>(.*?)</h1>')  # 匹配书名
findAbstract = re.compile(r'<div class="text txtsummary">(.*?)</div>', re.S)  # 匹配摘要
findPic = re.compile('<div class="pic"><img alt=.* src="(.*?)".*</div>')
findPage =re.compile('PageNo=(.+)',re.S)
Number = 0
baseurl = "http://military.people.com.cn"
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    'Referer': '  '
}


# 2.分析数据
def getData(baseurl):
    count =0
    pic_path = "./" + keyword  # 创建存放图片的文件夹
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)
    datalist = []
    html = askURL(baseurl+'.html')
    # print(html)
    bs = BeautifulSoup(html, "html.parser")
    page = bs.find(text=findPage)
    page=int(re.sub('\D','',page))
    for i in range(0, page):
        url = baseurl + str(i + 1) + '.html'
        html = askURL(url)
        bs= BeautifulSoup(html,"html.parser")
        newlist = bs.find_all(class_="list_16 mt10")
        newlist =str(newlist)
        newlist = re.findall(findNewurl,newlist)  #获得每页的新闻链接
        # print(type(newlist))


        # 2.逐一解析数据
        for item in newlist:  # 查找符合要求的字符串，形成列表
            data=[]
            item = str(item)
            newurl = baseurl+item
            html = askURL(newurl)
            # print(html)
            bs = BeautifulSoup(html,"html.parser")

            title = re.findall(findTitle, html)[0] #标题
            # print(title)
            count += 1
            print(count)
            data.append(title)

            author = bs.find_all(id_="p_editor")
            print(author)
            print(type(author))
            break
        break


        #     break
        #     data = []
    #         item = str(item)
    #         bookid = re.findall(findBookId, item)
    #         bookid = str(bookid)
    #         bookid = re.sub("[\'\[\]]", '', bookid)
    #         burl = bookurl + bookid
    #         # print(burl)
    #         bookhtml = askURL(burl)
    #         bs = BeautifulSoup(bookhtml, 'html.parser')

    #         # 标题信息
    #         title = re.findall(findTitle, bookhtml)[0]
    #         print(title)
    #         count += 1
    #         print(count)
    #         data.append(title)

    #         # 属性（作者，出版社，出版日期）
    #         total = bs.select("table>tbody>tr>td~td")
    #         author = str(total[0])
    #         author = re.sub("[<>td/著编]", "", author)
    #         # print(author)
    #         data.append(author)

    #         publish_house = str(total[1])
    #         publish_date = str(total[6])
    #         publish_house = re.sub("[<>td/]", "", publish_house)
    #         publish_date = re.sub("[<>td/clas=\"r]", "", publish_date)
    #         publish_date = re.sub('-', '/', publish_date)
    #         # print(publish_house)
    #         # print(publish_date)
    #         data.append(publish_house)
    #         data.append(publish_date)

    #         # 摘要
    #         abstract = re.findall(findAbstract, bookhtml)[0]
    #         # print(abstract)
    #         data.append(abstract)

    #         # 封面

    #         pic = bs.select('[class="pic"]')
    #         pic = re.findall(findPic, str(pic))
    #         pic = str(pic)
    #         pic = re.sub("[\[\]\'\"]", '', pic)
    #         title = re.sub("[*\\\/?<>|]", '', title)
    #         # print(pic)
    #         pic_name = str(count)+'.'+title + '.jpg'

    #         res = requests.get(pic, headers=head)
    #         time.sleep(0.3)
    #         with open(pic_path + '/' + pic_name, 'wb') as f:
    #             if res.status_code == 200:
    #                 try:
    #                     f.write(res.content)
    #                     data.append(pic_path + '/' + pic_name)
    #                 except (FileNotFoundError, FileExistsError):
    #                     print("第%d本书-%s" % (count, title))
    #                     continue
    #             else:
    #                 print('%s''异常' % title)
    #         # print(pic)
    #         datalist.append(data)
    #         # print(datalist)
    #         # break
    # # print(datalist)
    # # return datalist




# 1.爬取网页

def askURL(url):
    req = urllib.request.Request(url, headers=head)
    html = ""

    try:
        resp = urllib.request.urlopen(req)
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
    worksheet = workbook.add_sheet(keyword, cell_overwrite_ok=True)
    col = (' ', "title", "author", "source", "publish_date", "content")
    for i in range(0, 6):
        worksheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        if datalist[i] :
            print("第%d条" % (i + 1))
            data = datalist[i]
            worksheet.write(i + 1, 0, i + 1)
            for j in range(0, 5):
                worksheet.write(i + 1, j + 1, data[j])
        else:
            break

    workbook.save(savepath)

    print("save")


if __name__ == '__main__':
    main()

