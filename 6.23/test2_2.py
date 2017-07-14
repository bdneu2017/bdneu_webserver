#-*- coding:utf-8 -*-
import sys,os,psutil,time,MySQLdb,re,logging,threading,msvcrt
class GetSystemInformation(object):#获取系统信息的类
    def __init__(self):
        pass

    def OutputInformation(self,request):
        if request=='time':
            return self.time_info()
        elif request=='cpu':
            return self.cpu_info()
        elif request=='memory':
            return self.mem_info()
        elif request=='disk':
            return self.disk_info()
        elif request=='network':
            return self.network_info()
        else:
            print "Information is not exist"
            return None

    def time_info(self):
        print time.strftime('%a,%d,%b,%Y,%H:%M:%S',time.localtime())
        return time.strftime('%a,%d,%b,%Y,%H:%M:%S',time.localtime())
            
    def cpu_info(self):#获取cpu占用率
        cpu_state=psutil.cpu_percent(None)
        print u"CPU:%s %%" %cpu_state
        return cpu_state

    def mem_info(self):#获取内存占用率
        mem_info=psutil.virtual_memory()
        print u"Memory:%s %%" %mem_info.percent
        return mem_info.percent

    def disk_info(self):#获取磁盘使用率
        disk_temp=0
        count=0
        for id in psutil.disk_partitions():
            if 'cdrom' in id.opts or id.fstype=="":
                continue
            disk_name=id.device.split(':')
            s=disk_name[0]
            disk_info=psutil.disk_usage(id.device)
            disk_temp+=disk_info.percent/1
            count+=1
            print u"%s disk:%s %%" %(s,disk_info.percent)
        print u"Total disk:%s %%" %(disk_temp/count)
        return disk_temp/count

    def network_info(self):#获取网口速率
        netA=psutil.net_io_counters()
        tempA=(netA.bytes_recv+netA.bytes_sent)/1024
        time.sleep(1)
        netB=psutil.net_io_counters()
        tempB=(netB.bytes_recv+netB.bytes_sent)/1024
        bytes=tempB-tempA
        print u"Network bytes:%s kb/s" %bytes
        return bytes