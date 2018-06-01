#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import urllib2
from cloudxns.api import *
try:
    import json
except ImportError:
    import simplejson as json

if __name__ == '__main__':

	#获取本地网卡内网IP
	def getLocalIp(ifname = 'wlan0'):
		import socket, fcntl, struct;
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]));
		ip = socket.inet_ntoa(inet[20:24]);
		return ip;

	#在特定局域网中才执行
	if getLocalIp() == "192.168.1.123":
		#cloudxnsAPI密钥，API申请：https://www.cloudxns.net/AccountManage/apimanage.html
		api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		secret_key = 'xxxxxxxxxxxxxxxx'
		#获取外网IP
		url="http://members.3322.org/dyndns/getip"
		response = urllib2.urlopen(url)
		newip=response.read().strip()
		#print "外网IP:"+newip

		def updateIp():
			f = file("/home/pi/domoticz/scripts/python/ip.txt","wt")
			f.write(newip)
			f.close()
			#print "新IP已写入"
			#print 'CloudXNS API Version: ', Api.vsersion()
			api = Api(api_key=api_key, secret_key=secret_key)
			#api.ddns('home.dt27.cn')
			result = api.ddns('home.dt27.cn')
			#print result

		#判断本地IP文件是否存在
		if os.path.isfile("/home/pi/domoticz/scripts/python/ip.txt"):
			#文件存在时判断旧IP是否跟新IP一样
			f = file("/home/pi/domoticz/scripts/python/ip.txt","rt")
			oldip = f.readline()
			#print "旧IP:"+oldip

			if oldip == newip:
				f.close()
				#print "IP无变化"
			else:
				#不一样时，更新域名并重写IP文件
				updateIp()
		else:
			#本地IP文件不存在，直接更新域名并写入IP文件
			updateIp()
