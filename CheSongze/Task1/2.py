#coding=utf-8
import os
from multiprocessing import Process
import time
import psutil

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
    def Check(self,interval):
        """Retrieve raw stats within an interval window."""
        tot_before = psutil.net_io_counters()
        pnic_before = psutil.net_io_counters(pernic=True)
        #显示间隔
        time.sleep(interval)
        tot_after = psutil.net_io_counters()
        pnic_after = psutil.net_io_counters(pernic=True)
        #CPU
        self.data["cpu"] = "CPU: " + str(psutil.cpu_percent(interval)) + "%"
        #内存
        self.data["memory"] = u"Memory: %s %%" % psutil.virtual_memory().percent
        #硬盘
        self.data["disk"] = {}
        for id in psutil.disk_partitions():
            self.data["disk"][id.device.split(':')[0]] = psutil.disk_usage(id.device).percent
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

    def refresh_window(self):
        os.system("cls")
        """Print stats on screen."""
        print("")
        #时间 #CPU #内存
        print(time.asctime() + " | " + self.data["cpu"] + " | " + self.data["memory"])
        print("")
        #按行输出硬盘
        for disk in self.data["disk"]:
            print u'%s Disk: %s %%' % (disk, self.data["disk"][disk])
        print("")
        
        # 网络总数据
        print("NetStates:")
        print("total bytes:           sent: %-10s   received: %s" \
            % (self.data["total_net"]["upload_bytes"],
               self.data["total_net"]["download_bytes"]))
        print("pre-sec bytes:         sent: %-10s   received: %s" \
            % (self.data["total_net"]["upload_bytes_speed"],
               self.data["total_net"]["download_bytes_speed"]))
        print("total packets:         sent: %-10s   received: %s" \
            % (self.data["total_net"]["upload_pkt"], self.data["total_net"]["download_pkt"]))
        print("pre-sec packets:       sent: %-10s   received: %s" \
            % (self.data["total_net"]["upload_pkt_speed"], self.data["total_net"]["download_pkt_speed"]))
        
        #各网络数据
        print("")
        for name in self.data["sub_net"]:
            templ = "%-28s %15s %15s"
            print(templ % (name, "TOTAL", "PER-SEC"))
            print(templ % (
                "bytes-sent",
                self.data["sub_net"][name]["upload_bytes"],
                self.data["sub_net"][name]["upload_bytes_speed"]))
            print(templ % (
                "bytes-recv",
                self.data["sub_net"][name]["download_bytes"],
                self.data["sub_net"][name]["download_bytes_speed"]))
            print(templ % (
                "pkts-sent",
                self.data["sub_net"][name]["upload_pkt"],
                self.data["sub_net"][name]["upload_pkt_speed"]))
            print(templ % (
                "pkts-recv",
                self.data["sub_net"][name]["download_pkt"],
                self.data["sub_net"][name]["download_pkt_speed"]))
            print("")
    
    #功能进程
    def loop(self):
        while 1:
            interval = 1
            self.Check(interval)
            self.refresh_window()
            
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
