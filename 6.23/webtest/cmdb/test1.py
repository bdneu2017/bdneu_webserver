#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import HttpResponse
import sys, os, psutil, time
from django.shortcuts import render
SystemState = {'time': 0, 'cpu': 0, 'memory': 0, 'disk': 0, 'network': 0}
#startflag = 0  # 开始标记，使获取系统信息的线程先行起效
#endflag = 0  # 结束标记，置1时程序结束


class GetSystemInformation(object):  # 获取系统信息的类
    def __init__(self):
        pass

    def time_info(self):
        return time.strftime('%a,%d,%b,%Y,%H:%M:%S', time.localtime())

    def cpu_info(self):  # 获取cpu占用率
        cpu_state = psutil.cpu_percent(None)
        return cpu_state

    def mem_info(self):  # 获取内存占用率
        mem_info = psutil.virtual_memory()
        return mem_info.percent

    def disk_info(self):  # 获取磁盘使用率
        disk_temp = 0
        count = 0
        for id in psutil.disk_partitions():
            if 'cdrom' in id.opts or id.fstype == "":
                continue
            disk_name = id.device.split(':')
            s = disk_name[0]
            disk_info = psutil.disk_usage(id.device)
            disk_temp += disk_info.percent / 1
            count += 1
        return disk_temp / count

    def network_info(self):  # 获取网口速率
        netA = psutil.net_io_counters()
        tempA = (netA.bytes_recv + netA.bytes_sent) / 1024
        time.sleep(1)
        netB = psutil.net_io_counters()
        tempB = (netB.bytes_recv + netB.bytes_sent) / 1024
        bytes = tempB - tempA
        return bytes


def Get(request):  # 收集各个系统数据并显示在屏幕上

    funcGetSysInfo = GetSystemInformation()
    SystemState['time'] = funcGetSysInfo.time_info()
    SystemState['cpu'] = funcGetSysInfo.cpu_info()
    SystemState['memory'] = funcGetSysInfo.mem_info()
    SystemState['disk'] = funcGetSysInfo.disk_info()
    SystemState['network'] = funcGetSysInfo.network_info()
    return render(request, 'get.html', {'data': SystemState})
