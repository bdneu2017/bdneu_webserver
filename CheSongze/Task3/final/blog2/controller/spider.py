# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup 
import sys
from blog2 import app, db
from blog2.model.SpiderP9 import SpiderP9

reload(sys)
sys.setdefaultencoding('utf8')

#url = "http://psnine.com/"
#url = "http://www.qiushibaike.com/imgrank/"

def getsoup(url):
    #print(url)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    req = urllib2.Request(url, headers={
        'User-Agent': user_agent
    })
    response = urllib2.urlopen(req)
    content = response.read().decode('utf-8')
    #print(content)
    return BeautifulSoup(content, "lxml")

def qiubai(soup):
    items1 = soup.select("div.author a img")
    items2 = soup.select("a div.content span")
    items3 = soup.select("div.thumb a img")
    n = 0
    length1 = len(items1)
    length3 = len(items3)
    f=open("test.txt",'w')
    while n < length1:
        a=('作者信息：\n名称：'+items1[n]['alt']+'\n头像链接：'+items1[n]['src']+'\n\n')
        b=('段子信息：\n段子：'+items2[n].text+'\n')
        #以免有些没有图片的段子报错
        if n < length3:
            c=('段子图片链接：'+items3[n]['src']+'\n\n\n')
        else:
            c=('\n\n\n')
        print a
        print b
        print c
        f.write(a)
        f.write(b)
        f.write(c)
        n += 1
    f.close()
    print items1[0]['alt']
    print items1[0]
    return

def p9(soup):
    titles = soup.select("div.title")#标题
    urls = soup.select("div.title a")#网址
    comnums = soup.select("li a.rep")#回帖数
    users=soup.select("div a.psnnode")#发帖人
    tags=soup.select("div.meta")#标签
    n = 0
    f=open("test.txt",'w')
    taggroup=[]
    while n < min(20,len(titles)):
        p9=SpiderP9()
        p9.title = titles[n].text
        p9.url = urls[n]['href']
        p9.com = comnums[n].text
        p9.user= users[n].text
        tag=tags[n].select("a.node")#标签按条分类
        taggroup.append("")
        '''
        f.write(title+'\n')
        f.write(url+'\n')
        f.write(comnum+'\n')
        f.write(user+'\n')
        '''
        for t in tag:
            '''
            if t is tag[-1]:
                f.write(str(t.text)+'\n\n')#最后一条标签
            else:
                f.write(str(t.text)+', ')
            '''
            taggroup[n]=taggroup[n]+" "+str(t.text)
        p9.tag=str(taggroup[n])
        #p9=SpiderP9(title,url,comnum,user,str(taggroup[n]))
        db.session.add(p9)
        db.session.commit()
        n += 1
    f.close()
    return
'''
soup=getsoup(url)
#qiubai(soup)
p9(soup)
'''



'''
tags=soup.select("div.meta")#标签
n=0
f=open("test.txt",'w')
while n < len(tags):
    #print(type((tags[n])))
    print((tags[n]))
    tag=tags[n].select("a.node")
    for t in tag:
        if t is tag[-1]:
            f.write(str(t.text)+'\n')
        else:
            f.write(str(t.text)+', ')
    n=n+1
'''
'''
items1 = soup.select("div.title")
items2 = soup.select("div.title a")
#items1 = soup.select("a div.content span")
a=items1[0]
#print type(a)
#for item in a.__dict__:
#    print item+': '+str(a.__dict__[item])
#print a.__dict__
print a
print items2[0]['href']
print a.text
'''
'''
items1 = soup.select("div.author a img")
items2 = soup.select("a div.content span")
items3 = soup.select("div.thumb a img")
print items1[1]
print items2[1]
print items3[1]
'''