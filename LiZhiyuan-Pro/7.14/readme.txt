一：学习scrapy框架
    Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。
       HTML, XML源数据 选择及提取 的内置支持
       提供了一系列在spider之间共享的可复用的过滤器(即 Item Loaders)，对智能处理爬取数据提供了内置支持。
       通过 feed导出 提供了多格式(JSON、CSV、XML)，多存储后端(FTP、S3、本地文件系统)的内置支持
       提供了media pipeline，可以 自动下载 爬取到的数据中的图片(或者其他资源)。
       高扩展性。您可以通过使用 signals ，设计好的API(中间件, extensions, pipelines)来定制实现您的功能。
       内置的中间件及扩展为下列功能提供了支持
    常用命令：
    1.scrapy项目生成，项目管理
    命令：scrapy startproject projectname

    2.根据模板生成爬虫。
    命令：scrapy genspider [-t template] <name> <domain>
    
    3.利用写好的怕虫进行爬取
    命令：scrapy crawl spidername
 
二：学习xpath语言
    XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。
    利用scrapy spider爬取到html页面，需要从页面中提取出我们需要的信息，这时候就需要xpath语法构造选择器。
    在测试你的xpath语句时，可以通过scrapy shell命令来打开一个终端，在里面测试各种xpath语句。

三：git学习
  1、git是一个版本控制软件，与svn类似，特点是分布式管理，不需要中间总的服务器，可以增加很多分支。

  2、windows下可以使用git for windows，有git bash，git Gui，git cmd。

  3、git bash ，git cmd只是终端操作，git Gui是图形化管理界面。都用过后我更喜欢git bash的使用。

  4、git需要一个仓库来放项目，这个仓库可以放在某一个任何一个安装了git的电脑上。也可以使用网上的仓库。

  5、网上的git仓库比较好的是github。

  6、一般项目会在一台服务器上做一个仓库，其他人下载，并实现分支。

  7、每次看github上的内容都要登陆了github，可以下载一个github的桌面版。并提供git shell。
  
  8、git教程我全部看了一遍，每个命令都测试了一遍，远程仓库部分也拿自己的github账号测试了一遍，包括一些常用命令：
	#添加当前修改的文件到暂存区  
	git add .  

  	#提交你的修改  
	git commit –m "你的注释" 

	#推送你的更新到远程服务器,语法为 git push [远程名] [本地分支]:[远程分支]  
	git push origin master  

	#查看文件状态  
	git status

	#查看提交的历史记录  
	git log  
	不一一列举了，除此之外还包括工作区，暂存区，本地git仓库，远程git仓库的管理和操作，还有各个区域版本
    回退等操作，我对git工作原理也有了更深的认识

此外，我还将自己的vps配置成git远程仓库，虽然最终使用的是github，但自己配置一遍还是有很多的收获。

下周将爬虫优化整合到django web项目中，并适当美观web页面，优化功能模块。

