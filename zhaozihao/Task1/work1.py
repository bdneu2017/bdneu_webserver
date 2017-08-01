# encoding:utf-8
import os,shutil,re

def Checkfile(filepath):#检查文件是否存在
    if os.path.isfile(filepath):
        return 1
    else:
        return 0

def Readfile(filepath,pattern):#读取文件、正则表达式匹配、写入新文件
    fp1=open(filepath,"r")
    fp2=open("ip2.txt","w")
    for line in open(filepath):
        line=fp1.readline()
        str=re.findall(pattern,line)
        for i in str:
            print i
            fp2.write(i+'\n')
    fp2.close()
    fp1.close()
	
def main():#主函数、预设正则表达式
    pattern=re.compile(r'(?<![\.\d])(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])')
    filepath=raw_input("Input file path:")
    if Checkfile(filepath):
        Readfile(filepath,pattern)
    else:
        return "ERROR"
			
if __name__ == "__main__":
	main()