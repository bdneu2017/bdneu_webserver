# encoding:utf-8
#-*-coding:utf-8-*-
'''
Created on 2017年6月21日

@author: David
'''

import psutil
import time
#from test.test_zipimport_support import ZipSupportTests
from multiprocessing import Process
import os

#获取网卡流量信息
def get_key():
    nics = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称
    recv = {}
    sent = {}
    for key in nics:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数
    return nics, recv, sent
    
# 函数计算每秒速率
def get_rate(func):
    nics,old_recv,old_sent = func()  # 上一秒收集的数据
    time.sleep(1)
    nics,now_recv,now_sent = func()  # 当前所收集的数据
 
    net_in = {}
    net_out = {}
    for key in nics:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024) # 每秒发送速率
    return nics, net_in, net_out

def getSysInfo():
    info={}
    #获取cpu实时占用率
    info['cpu']=psutil.cpu_percent()
    
    #获取内存实时使用率
    info['memory']=psutil.virtual_memory().percent
    
    #获取各分区使用情况
    i=len(psutil.disk_partitions())
    for i in range(0,i):
        c=psutil.disk_partitions()[i].device
        info.setdefault('disk',{})[c]=psutil.disk_usage(c).percent
        
    #获取各网口实时流量
    nics,net_in,net_out=get_rate(get_key)
    for key in nics:
        #print('%s\nInput:\t %-5sKB/s\nOutput:\t %-5sKB/s\n' % (key, net_in.get(key), net_out.get(key)))
        info.setdefault('net',{})[key]={'入流量':net_in.get(key),'出流量':net_out.get(key)}
    return info
    
# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...'% (name, os.getpid()))
    while 1:
        #print(time.asctime())
        #print(datetime.datetime.now())
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print(getSysInfo())
        time.sleep(1)
    

def main():
    #print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('"Get system info"',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
    
if __name__ == '__main__':
    #getSysInfo()
    main()