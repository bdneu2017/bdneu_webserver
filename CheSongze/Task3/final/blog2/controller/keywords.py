# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
from blog2 import app, db
from blog2.model.Keywords import Keywords
from mail import send_email
'''
def findSubstrings(substrings,destString):
    #res =  map(lambda x:str([destString.index(x),x]),filter(lambda x:x in destString,substrings))
    res =  map(lambda x:str([destString.index(x),x]),['123456','123456'])
    if res:
        return ', '.join(list(res))

def isSubstring3(s1,s2):
    return s2 in s1

#def listsub(s2,s3,s1):
    return reduce(lambda x:re.sub(x,s3,s1),s2)
'''

def wordreplace(filt,content):
    for filter_word in filt:
        fw=filter_word.key.rstrip()
        if fw in content.title:
            fw_len=len(fw)
            content.title=content.title.replace(fw,'*'*fw_len)  
        if fw in content.content:
            fw_len=len(fw)
            content.content=content.content.replace(fw,'*'*fw_len)  
    return content

'''
#print findSubstrings(s2,s1)
#print filter(lambda x:re.findall(x,s1),s2)
#print filter(lambda x:x in s1,s2)
#print map(lambda x:re.findall(x,s1),s2)

#print s1.count('123456')
#print isSubstring3(s1,s2)
#print len(re.findall(s2,s1))
#print re.sub(s2,s3,s1)
#print listsub(s2,s3,s1)
'''
def keynum(content,key):
    '''
    for i in key:
        content.count(i)'''
    text=content.title+' '+content.content
    mailcon=[]
    num=map(lambda x:text.count(x.key),key)
    #keydic=zip(key['key'],num)
    for i in range(len(key)):
        if num[i] != 0:
            key[i].times+=num[i]
            conlist={'key':key[i].key,'times':num[i]}
            if key[i].warning:
                mailcon.append(conlist)
    if mailcon:
        send_email(mailcon,content)
    #key.times=key.times+keydic[key['key']]
    return key

def keynum2(content,key):#更新用
    '''
    for i in key:
        content.count(i)'''
    text=content.title+' '+content.content
    key.times+=text.count(key.key)
    #key.times=key.times+keydic[key['key']]
    return key

def run():
    s1 = '123456789123456'
    s2 = ['123','456','789']
    #s3 = 'abc'
    user_input=raw_input('Leave your comments:  ')
    print map(lambda x:user_input.count(x),s2)#对应出现次数
    print wordreplace(s2,user_input)
    