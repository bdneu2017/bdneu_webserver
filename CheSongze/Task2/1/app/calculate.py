#coding=utf-8
import os
import sys
from multiprocessing import Process
import time
import psutil
from collections import OrderedDict


defaultencoding = 'gbk'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)

class SysCheck(object):
    data = {}
    printline= []
    pdata={}
    def Check(self,interval):
        """Retrieve raw stats within an interval window."""
        tot_before = psutil.net_io_counters()
        pnic_before = psutil.net_io_counters(pernic=True)
        #显示间隔
        time.sleep(interval)
        tot_after = psutil.net_io_counters()
        pnic_after = psutil.net_io_counters(pernic=True)
        #CPU
        self.data["cpu"] = str(psutil.cpu_percent(interval)) + "%"
        #内存
        self.data["memory"] = str(psutil.virtual_memory().percent)+"%"
        self.data["line1"]=(time.asctime() + " | " + self.data["cpu"] + " | " + self.data["memory"])
        #硬盘
        self.data["disk"] = OrderedDict()
        for id in psutil.disk_partitions():
            self.data["disk"][id.device.split(':')[0]] = str(psutil.disk_usage(id.device).percent)+"%"
        #网络总数据
        self.data["total_net"] = {}
        self.data["total_net"]["upload_bytes"] = bytes2human(tot_after.bytes_sent)
        self.data["total_net"]["download_bytes"] = bytes2human(tot_after.bytes_recv)
        self.data["total_net"]["upload_pkt"] = tot_after.packets_sent
        self.data["total_net"]["download_pkt"] = tot_after.packets_recv
        self.data["total_net"]["upload_bytes_speed"] = bytes2human(tot_after.bytes_sent - tot_before.bytes_sent) + '/s'
        self.data["total_net"]["download_bytes_speed"] = bytes2human(tot_after.bytes_recv - tot_before.bytes_recv) + '/s'
        self.data["total_net"]["upload_pkt_speed"] = str(tot_after.packets_sent - tot_before.packets_sent)+"/s"
        self.data["total_net"]["download_pkt_speed"] = str(tot_after.packets_recv - tot_before.packets_recv)+"/s"
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
            self.data["sub_net"][name]["upload_pkt_speed"] = str(stats_after.packets_sent - stats_before.packets_sent)+"/s"
            self.data["sub_net"][name]["download_pkt_speed"] = str(stats_after.packets_recv - stats_before.packets_recv)+"/s"

    def refresh_window(self):
        """print stats on screen."""
        self.printline= []
        #时间 #CPU #内存
        self.pdata["time"]=time.asctime()
        self.pdata["cpu"]=self.data["cpu"]
        self.pdata["memory"]=self.data["memory"]
        #按行输出硬盘
        self.pdata["disk"]=self.data["disk"]
        
        # 网络总数据
        self.pdata["total_bytes"]={}
        self.pdata["total_bytes_speed"]={}
        self.pdata["total_pkt"]={}
        self.pdata["total_pkt_speed"]={}
        self.pdata["total_bytes"]["sent"]=self.data["total_net"]["upload_bytes"]
        self.pdata["total_bytes"]["resv"]=self.data["total_net"]["upload_bytes"]
        self.pdata["total_bytes_speed"]["sent"]=self.data["total_net"]["upload_bytes_speed"]
        self.pdata["total_bytes_speed"]["resv"]=self.data["total_net"]["upload_bytes_speed"]
        self.pdata["total_pkt"]["sent"]=self.data["total_net"]["upload_pkt"]
        self.pdata["total_pkt"]["resv"]=self.data["total_net"]["upload_pkt"]
        self.pdata["total_pkt_speed"]["sent"]=self.data["total_net"]["upload_pkt_speed"]
        self.pdata["total_pkt_speed"]["resv"]=self.data["total_net"]["upload_pkt_speed"]
        
        #各网络数据
        self.pdata["sub_net"]=self.data["sub_net"]


    #运行
    def __init__(self): 

        #启动主进程
        interval=1
        self.Check(interval)
        self.refresh_window()

if __name__ == '__main__':
    SysCheck()
