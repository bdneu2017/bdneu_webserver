# encoding:utf-8
#-*-coding:utf-8-*-
'''
Created on 2017年6月21日

@author: David
'''
import re

def findIP():
    fp=open('ip','r')
    fe=open('findip.txt','a')
    pattern=r'(1\d{2}|\d{1,2}|2[0-5]{2})\.(1\d{2}|\d{1,2}|2[0-5]{2})\.(1\d{2}|\d{1,2}|2[0-5]{2})\.(1\d{2}|\d{1,2}|2[0-5]{2})'
    cr=re.compile(pattern)  
    ip=''
    for line in fp.readlines():
        result=cr.findall(line)
        if(len(result)>0):
            for i in range(0,len(result)):
                for j in range(3):
                    ip=ip+result[i][j]+'.'
                ip+=result[i][3]+'\n'
    print('Find ips as followed:\n'+ip)          
    fe.write(ip)
    fp.close()
    fe.close()
def main():
    findIP()
    
if __name__ == '__main__':
    #pass
    main()