#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import urllib2
from time import sleep
from threading import Thread

#此脚本在树莓派上运行正常
#无需定时执行，仅设置开机启动即可
#需要先安装Python模块urllib2
#局域网设备扫描使用arp-scan
#由于iOS设备的wifi休眠特性，设备离线时无法立即判定离线

#Domoticz服务器地址及端口号
domoticzserver = "127.0.0.1:8080"
#此方法向Domoticz服务器发送请求
def domoticzrequest (url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response.read()

# 要检测的设备
device = ["myPhone","herPhone"]

# 设备是否会将WIFI休眠，iOS设备请设置1
type = ["0","1"]

# 设备MAC地址
address = ["00:00:00:00:00:00","00:00:00:00:00:00"]

# 设备在Domoticz中对应虚拟开关的IDX
idxs = ["21","22"]

#延时，防止刚开机时获取失败
#print("30秒后开始运行")
sleep(30)

# 记录设备状态
firstRun = [1] * len(device)
presentSent = [0] * len(device)
notPresentSent = [0] * len(device)
counter = [0] * len(device)


# Function that checks for device presence
def whoIsHere(i):

    #print("休息30秒，以供主线程完成arp-scan并输出")
    sleep(30)

    # Loop through checking for devices and counting if they're not present
    while True:

        # 键盘输入后退出
        if stop == True:
            print "退出"
            exit()
        else:
            pass

        # 设备在线
        #print("开始分析output数据")
        if address[i] in output:
            # 检测到设备在线
            #print(device[i] + " 已连接"+bytes(i))
            if presentSent[i] == 0:
                # 向外输出
                #print(device[i] + " 向外输出设备在线")
                domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=switchlight&idx="+idxs[i]+"&switchcmd=On")
                # Reset counters so another stream isn't sent if the device
                # is still present
                firstRun[i] = 0
                presentSent[i] = 1
                notPresentSent[i] = 0
                counter[i] = 0
                #print("输出在线状态后休息15分钟")
                sleep(900)
            else:
                #print("之前已向外输出，重置计数器并休息15分钟")
                counter[i] = 0
                sleep(900)
        else:
            #print(device[i] + " 离线"+bytes(i))
            
            # Wifi会休眠的设备
            if type[i] == 1:
                # 第一次执行或累计15分钟内30次扫描均离线
                if counter[i] == 30 or firstRun[i] == 1:
                    firstRun[i] = 0
                    if notPresentSent[i] == 0:
                        # 未发送离线状态
                        #print(device[i] + " 向外输出设备离线")
                        domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=switchlight&idx="+idxs[i]+"&switchcmd=Off")
                        # 设置已输出
                        notPresentSent[i] = 1
                        presentSent[i] = 0
                        counter[i] = 0
                    else:
                        # 发送过离线状态
                        counter[i] = 0
                        sleep(30)

                else:
                    # Count how many 30 second intervals have happened since the device
                    # disappeared from the network
                    counter[i] = counter[i] + 1
                    #print(device[i] + "计数器 " + str(counter[i]))
                    #print("休息30秒")
                    sleep(30)
            else:
                # 第一次执行或累计5分钟内10次扫描均离线
                if counter[i] == 10 or firstRun[i] == 1:
                    firstRun[i] = 0
                    if notPresentSent[i] == 0:
                        # 未发送离线状态
                        #print(device[i] + " 向外输出设备离线")
                        domoticzrequest("http://"+domoticzserver+"/json.htm?type=command&param=switchlight&idx="+idxs[i]+"&switchcmd=Off")
                        # 设置已输出
                        notPresentSent[i] = 1
                        presentSent[i] = 0
                        counter[i] = 0
                    else:
                        # 发送过离线状态
                        counter[i] = 0
                        sleep(30)

                else:
                    # Count how many 30 second intervals have happened since the device
                    # disappeared from the network
                    counter[i] = counter[i] + 1
                    #print(device[i] + "计数器 " + str(counter[i]))
                    #print("休息30秒")
                    sleep(30)


# Main thread
try:
    global stop
    stop = False

    # Start the thread(s)
    for i in range(len(device)):
        t = Thread(target=whoIsHere, args=(i,))
        #print("开始进程"+bytes(i))
        t.start()

    while True:
        global output
        # 获取局域网所有设备
        output = subprocess.check_output("sudo arp-scan --interface=wlan0 --localnet", shell=True)
        # 每次扫描间隔30秒
        #print("本次扫描结束并已输出到output，30秒后进行下一次扫描...")
        sleep(30)

except KeyboardInterrupt:
    stop = True
    exit()
