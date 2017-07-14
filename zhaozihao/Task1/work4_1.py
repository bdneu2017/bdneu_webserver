#-*- coding:utf-8 -*-
import sys,os,psutil,time,re,threading,msvcrt
list=('cpu:','memory:','disk:','network:')

def ChangeConfig():#修改阈值配置文件，按d进行修改，按其他任意键退出程序
    str=[0,0,0,0]
    while True:
        print "\nEnter 'd' or 'D' change config,if input other,the program will be exit"
        if ord(msvcrt.getch()) in [68,100]:
            print "Please Input threshold values of cpu,memory,disk and network"
            print "Format:cpu memory disk network"
            str[0],str[1],str[2],str[3]=raw_input("Input:").split()
            fp=open("config.txt","w")
            for line in range(4):
				fp.write(list[line]+str[line]+'\n')
            fp.close()
            print 'Change successful\n'
        else:
			break
					
if __name__=="__main__":
    p1=threading.Thread(target=ChangeConfig)
    p1.start()