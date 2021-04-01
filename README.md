# study
----------------------
初学github
--------------
##  Python爬虫学习进程

- 3月28日

- 	写读书网爬虫，目的爬取图书概括，关键词：西方战争
	
	- 	主要问题：
		- 1.正则表达式运用
		- 2.图片的反爬机制
		- 3.re库和bs4库运用
	
- 3月29日

- 基本上以修改补全28日代码，将关键词搜索改为分类爬取

  - 主要问题：

    - 1.细节处理
      
    - 2.异常处理   大量爬取，不设置sleep参数，会发生超时，图片文件保存出错过。    

      ​			问题描述：OSError: [Errno 22] Invalid argument: './军事理论/1575.*运筹谋略.jpg'

      ​			问题原因：Windows文件名不允许英文输入法状态下的:":< > / \ | : " * ?"字符

      ​			解决方法：将获取的图书名进行过去，排除*号等。

    - 3.图片的爬取数量与总数不对应  	

      ​			问题原因：初步认定是选取的文件名存在某些不合法因素  

      ​			尝试方案：在文件名前面加上序号

- 3月30日

- 进一步细化完善读书网爬虫代码，基本上实现了读书网二级分类下数据的有效爬取

	- 说明：
	- 	1.将baseurl替换为想要爬取的二级目录链接，格式参考现有。
	- 	2.在getdata函数中将range第二个参数改为分类下数据页数。
	- 	3.为避免网站识别拒绝响应，产生超时错误，建议time.sleep(0.4)以上
	
- 3月31日

  - 昨晚和今天，在跟老师讨论爬取数据源的问题，鉴于甲方的要求和实际情况差异，讨论开会进行了很长时间。今天的代码没写完，最近这几天太多心思放在这上面了，课程方面落下的有点多。鉴于我自己的情况，要放慢代码的更新换代，先把课程内容补上来先。
  - 今天的代码放个半成品，明天继续写。

- 4月1日
  - 今天把人民网军事的代码完善了一下，分类测试没问题，从21点到23点都在debug整合后整个板块的代码
  - 后期只需要把日期筛选加上就可以保持更新了。
  - 这两天没有什么新的收获，课程拉下的也没补上。每天忙归忙，进步基本没有。