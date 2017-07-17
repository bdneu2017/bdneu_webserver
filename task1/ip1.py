#!/usr/bin/env python
# coding:utf-8
import re
r=open('ip.txt','r')
result=''#result is str
for line in r.readlines():
    result1=re.findall('^([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])$',line)#match the legal ip in line
    if not result1==[]:#there is result in the line
        print result1[0]
        for i in range(len(result1[0])-1): #ip format         
            result=result+result1[0][i]+'.'
        result=result+result1[0][i+1]+'\n'
w=open('legal_ip.txt','w')
w.write(result)#write the legal ip to a file
w.close()
r.close()