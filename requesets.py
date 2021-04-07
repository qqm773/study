# -*- codeing = utf-8 -*-
# @Time : 2021/4/6 22:27
# @Author : 疏苑
# @File : requesets.py
# @Software : PyCharm

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree #xpath 解析器
import xlwt

main_url = "http://junshi.xilu.com/"
keyword = "军事"
savepath = "媒体文章表_分类_" + keyword +"_来源_西陆网.xls"
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Referer": "http://www.xilu.com/"
}
findNewurl = re.compile(r'<a href="(http://.*?.html)".*?</a>', re.S)


def main():
    datalist = getdata(main_url)
    saveDate(datalist , savepath)


def getdata(main_url):
    datalist = []
    res = askurl(main_url)

    bs = BeautifulSoup(res, 'lxml')
    new = bs.select('div > ul > li > a')
    new = str(new)
    newurl = re.findall(findNewurl, new)
    for item in newurl:
        data = []
        # print(item)
        resp = askurl(item)
        bs = BeautifulSoup(resp, 'lxml')
        title = bs.select('div > h1 > span')[0].string
        print(title)
        data.append(title)
        total = bs.select('div >div> div >div>div  div [class]',limit=4)
        source = re.sub('来源：','',total[1].string)
        author = re.sub('作者：',"",total[2].string)
        date = re.sub('-','/',total[3].string[:10])
        # print(source)
        # print(author)
        # print(date)
        data.append(author)
        data.append(source)
        data.append(date)
        # tree = etree.HTML(resp)
        # li_list=tree.xpath('//div[@class="pagination f14"]/a')
        # for item in li_list:
        #     print(item)
        # print(li_list)
        data1 = []
        for i in range(1,20):
            item1 = re.sub('\.html','_',item)
            item1 = item1+str(i)+'.html'
            resp1 = askurl(item1)
            bs1 = BeautifulSoup(resp1, 'lxml')
            # print(item1)
            # tree = etree.HTML(resp1)
            # li_list=tree.xpath('//div[@class="contain_detail_cnt f18"]/p/text()')
            # if li_list ==[]:
            #     break
            # li_list=str(li_list)
            # li_list=re.sub('[rn\]\[\\\]','',li_list)
            # data1.append(li_list)
            content = bs1.find('div',class_='contain_detail_cnt f18')
            content = content.select('p~p')
            if content == []:
                break
            content = str(content)
            content = re.sub('<.*?>', '', content)
            content = re.sub(',', '', content)
            data1.append(content)
            data1.append('\n')
            # print(content)
        # data1=str(data1)
        # data1=re.sub('[\[\]]','',data1)
        data.append(data1)
        data.append(keyword)
        # print(total)
        # print(data)
        datalist.append(data)
        # break
    print(datalist)
    return datalist


def askurl(url):
    response = requests.get(url=url, headers=head)
    response.encoding = 'utf-8'
    # print(response.text)
    return response.text


def saveDate(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # global jk
    worksheet = workbook.add_sheet(keyword, cell_overwrite_ok=True)
    col = (' ', "title", "author", "source", "publish_date", "content", "tag")
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

    print("save")


if __name__ == '__main__':
    main()
