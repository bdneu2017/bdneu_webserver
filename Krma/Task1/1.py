# encoding: UTF-8
import re

def openfile(name):
    flag=0
    for line in open(name):
        flag=flag+matchIP(line)
    return flag

def matchIP(ip):
    #matchIP = re.findall( r'((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)', ip)
    #matchIP = re.findall( r'((0|25[0-5]\.|2[0-4]\d\.|1\d\d\.|[1-9]\d\.|\d\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)', ip)
    #matchIP = re.findall( r'(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', ip)
    #matchIP = re.findall( r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)', ip)
    #pattern=r'(?:(?:0|2(?:5[0-5]|[0-4]\d)|1?\d{1,2})\.){3}(?:0|2(?:5[0-5]|[0-4]\d)|1?\d{1,2})'
    #cr=re.compile(pattern)
    #matchIP=cr.findall(ip)
    matchIP = re.findall( r'(?:(?:2(?:5[0-5]|[0-4]\d)|1\d{2}|[1-9]?\d)\.){3}(?:0|2(?:5[0-5]|[0-4]\d)|1?\d{1,2})',ip)
    if matchIP:
        for IP in matchIP:
            print(IP)
        return 1
    else:
        return 0

#test="abc123.2.3.4cdx4.3.2.1fjyli255.135.4.12gkuiug0.256.1.1pr"
filename="test.txt"
if not openfile(filename):
    print("NO Match IP.")
