#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',9090))

msg = '1,S1,1,80'  #strip默认取出字符串的头尾空格
client.send(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
print('recv:',data.decode()) #输出我接收的信息
time.sleep(2)
msg = '1,C1,1,90'  #strip默认取出字符串的头尾空格
client.send(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
print('recv:',data.decode()) #输出我接收的信息

msg = 'X------'  #strip默认取出字符串的头尾空格
client.send(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
client.close() #关闭这个链接