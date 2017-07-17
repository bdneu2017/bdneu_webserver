#coding=utf-8
import os
from multiprocessing import Process
import time
import json
import logging
import psutil
import MySQLdb


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%-6.2f %s' % (value, s)
    return '%-6.2f B' % (n)

class SysCheck(object):
    #任务四附加 用于检测是否超过阈值
    def checkThreshold(self):
        warning = ''
        threshold_cpu = 20
        threshold_mem = 20
        threshold_disk = 70
        logging.basicConfig(level = logging.DEBUG,
                            format = '%(asctime)s %(filename)s[line:%(lineno)d] %(process)s %(funcName)s %(levelname)s %(message)s',
                            datefmt = '%a, %d %b %Y %H:%M:%S',
                            filename = 'warinng.log',
                            filemode = 'w')
        
        if self.data['cpu'] >= threshold_cpu:
            logging.warning('cpu is in risk')
            warning += '|CPU'
        if self.data['memory'] >= threshold_mem:
            logging.warning('memory is in risk')
            warning += '|Memory'

        for name in self.data['disk'].keys():
            if self.data['disk'][name] > threshold_disk:
                logging.warning('disk '+name+' is in risk')
                warning += '|Disk '+name
        warning += '|'
        return warning
    data = {}
    flag = 0
    def Check(self,interval):
        """Retrieve raw stats within an interval window."""
        tot_before = psutil.net_io_counters()
        pnic_before = psutil.net_io_counters(pernic=True)
        #显示间隔
        time.sleep(interval)
        tot_after = psutil.net_io_counters()
        pnic_after = psutil.net_io_counters(pernic=True)
        #CPU
        self.data["cpu"] = psutil.cpu_percent(interval)
        #内存
        self.data["memory"] = psutil.virtual_memory().percent
        #硬盘
        self.data["disk"] = {}
        for id in psutil.disk_partitions():
            self.data["disk"][id.device.split(':')[0]] = str(psutil.disk_usage(id.device).percent)
        #网络总数据
        self.data["total_net"] = {}
        self.data["total_net"]["upload_bytes"] = bytes2human(tot_after.bytes_sent)
        self.data["total_net"]["download_bytes"] = bytes2human(tot_after.bytes_recv)
        self.data["total_net"]["upload_pkt"] = tot_after.packets_sent
        self.data["total_net"]["download_pkt"] = tot_after.packets_recv
        self.data["total_net"]["upload_bytes_speed"] = bytes2human(tot_after.bytes_sent - tot_before.bytes_sent) + '/s'
        self.data["total_net"]["download_bytes_speed"] = bytes2human(tot_after.bytes_recv - tot_before.bytes_recv) + '/s'
        self.data["total_net"]["upload_pkt_speed"] = tot_after.packets_sent - tot_before.packets_sent
        self.data["total_net"]["download_pkt_speed"] = tot_after.packets_recv - tot_before.packets_recv
        #各网络数据
        nic_names = pnic_after.keys()
        nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
        self.data["sub_net"] = {}
        for name in nic_names:
            self.data["sub_net"][name] = {}
            stats_before = pnic_before[name]
            stats_after = pnic_after[name]
            self.data["sub_net"][name]["upload_bytes"] = bytes2human(stats_after.bytes_sent)
            self.data["sub_net"][name]["download_bytes"] = bytes2human(stats_after.bytes_recv)
            self.data["sub_net"][name]["upload_pkt"] = stats_after.packets_sent
            self.data["sub_net"][name]["download_pkt"] = stats_after.packets_recv
            self.data["sub_net"][name]["upload_bytes_speed"] = bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s'
            self.data["sub_net"][name]["download_bytes_speed"] = bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s'
            self.data["sub_net"][name]["upload_pkt_speed"] = stats_after.packets_sent - stats_before.packets_sent
            self.data["sub_net"][name]["download_pkt_speed"] = stats_after.packets_recv - stats_before.packets_recv
    
    #连接数据库，把info信息和时间信息time_now写入数据库表
    def Conn2db(self):
        #连接数据库
        conn = MySQLdb.connect(host = 'localhost',
                               port = 3306, user = 'root',
                               passwd = 'root',
                               db = 'testdb')

        cursor = conn.cursor()
        #第一次会创建数据库info
        sql = '''CREATE TABLE IF NOT EXISTS INFO (
            `ID` int(10) NOT NULL AUTO_INCREMENT,
            `Time` varchar(30)  NOT NULL,
            `CPU` float NOT NULL,
            `Mem` float NOT NULL,
            `Disk` text(300) NOT NULL,
            `Upload` varchar(20) NOT NULL,
            `Download` varchar(20) NOT NULL,
            `Warning` text(600), 
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        AUTO_INCREMENT=1 ;'''
        cursor.execute(sql)
        if not self.flag:
            print("+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+")
            print("  ID  | Time                      |  CPU  |  Mem  | Disk                                              | Upload     | Download   | Warning")
            print("+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+")
            self.flag = 1
        #把info字典中的disk字典和net字典转成json格式然后存入数据库
        j_disk = json.dumps(self.data['disk'])[1:-1]
        #任务四中检测阈值更新warning
        warning = self.checkThreshold()
        j_warn = json.dumps(warning)[2:-2]
        sql = "insert into info (time,cpu,mem,disk,upload,download,warning) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (time.asctime(),
                        self.data["cpu"], self.data["memory"], j_disk,
                        self.data["total_net"]["upload_bytes_speed"],
                        self.data["total_net"]["download_bytes_speed"], j_warn))
        sql = 'select * from info order by id desc limit 1'
        cursor.execute(sql)
        for row in cursor.fetchall():
            print ("%5s | %-25s |  %4.1f |  %4.1f | %-49s | %-10s | %-10s | %s"%(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        conn.commit()
        cursor.close()
        conn.close()

    #功能进程
    def loop(self):
        while 1:
            interval = 1
            self.Check(interval)
            self.Conn2db()
            
    #运行
    def __init__(self): 

        #启动主进程
        print('Parent process %s.' % os.getpid())
        p = Process(target=self.loop, args=())
        print('Child process will start.')
        p.start()
        p.join()
        print('Child process end.')

if __name__ == '__main__':
    SysCheck()
