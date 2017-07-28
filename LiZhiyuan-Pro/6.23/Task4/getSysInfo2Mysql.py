# encoding:utf-8 
#-*-coding:utf-8-*-
'''
Created on 2017��6��21��

@author: David
'''

import os
import time
from multiprocessing import Process
from getSysInfo import getSysInfo
import pymysql
import json
import logging



#任务四附加 用于检测是否超过阈值
def checkThreshold(info):
    warning=''
    #自己设定一些阈值，为了方便检验是否有效，把cpu,mem阈值设置较小
    threshold_cpu=20
    threshold_mem=20
    threshold_disk=70
    threshold_net=10  #小于10KB/s认为需要发出警告
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(process)s %(funcName)s %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='warinng.log',
                filemode='w')
    
    if info['cpu']>=threshold_cpu:
        logging.warning('cpu is in risk')
        warning+='cpu,'
    if info['memory']>=threshold_mem:
        logging.warning('memory is in risk')
        warning+='memory,'
        
    for key1 in info['disk'].keys():
        if info['disk'][key1] > threshold_disk:
            logging.warning('disk '+key1+' is in risk')
            warning+='disk '+key1
    
    for key1 in info['net'].keys():
        for key2 in info['net'][key1].keys():
            if info['net'][key1][key2] < threshold_net:
                logging.warning(key1+key2+'is in risk')
                warning+='net'+key1               
     
    return warning

def run_proc(name):
    print('Run child process %s (%s)...'% (name, os.getpid()))
    while 1:
        now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(now)
        info=getSysInfo()
        conn2db(info,now)
        print(info)
        time.sleep(1)

#连接数据库，把info信息和时间信息time_now写入数据库表
def conn2db(info,time_now):
    #连接数据库
    conn=pymysql.connect(host='localhost',
                         port=3306,user='root',
                         passwd='lzy958',
                         db='systeminfo')
    
    
    cursor=conn.cursor()
    #第一次会创建数据库info
    sql = '''CREATE TABLE IF NOT EXISTS INFO (
        `id` int(10) NOT NULL AUTO_INCREMENT,
        `time` varchar(30)  NOT NULL,
        `cpu_percent` float(3,1) NOT NULL,
        `mem_percent` float(3,1) NOT NULL,
        `disk_percent` char(30) NOT NULL,
        `net` text(900) NOT NULL,
        `warning` text(600), 
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
    AUTO_INCREMENT=1 ;'''
    cursor.execute(sql)
    
    #把info字典中的disk字典和net字典转成json格式然后存入数据库
    j_disk=json.dumps(info['disk'])
    j_net=json.dumps(info['net'])
    
    #任务四中检测阈值更新warning
    warning=checkThreshold(info)
    j_warn=json.dumps(warning)
    sql="insert into info (time,cpu_percent,mem_percent,disk_percent,net,warning) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(time_now,info['cpu'],info['memory'],j_disk,j_net,j_warn))
    
    conn.commit()
    cursor.close()
    conn.close()
    
def main():
    p = Process(target=run_proc, args=('"Get system info"',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
    
if __name__ == '__main__':
    #pass
    main()