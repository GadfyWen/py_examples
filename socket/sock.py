 1 #!/usr/bin/env python
 2 #-*- coding:utf-8 -*-
 3 
 4 import socket
 5 import select
 6 import Queue
 7 
 8 #创建socket对象
 9 serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
10 #设置IP地址复用
11 serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
12 #ip地址和端口号
13 server_address = ("127.0.0.1", 8888)
14 #绑定IP地址
15 serversocket.bind(server_address)
16 #监听，并设置最大连接数
17 serversocket.listen(10)
18 print  "服务器启动成功，监听IP：" , server_address
19 #服务端设置非阻塞
20 serversocket.setblocking(False)  
21 #超时时间
22 timeout = 10
23 #创建epoll事件对象，后续要监控的事件添加到其中
24 epoll = select.epoll()
25 #注册服务器监听fd到等待读事件集合
26 epoll.register(serversocket.fileno(), select.EPOLLIN)
27 #保存连接客户端消息的字典，格式为{}
28 message_queues = {}
29 #文件句柄到所对应对象的字典，格式为{句柄：对象}
30 fd_to_socket = {serversocket.fileno():serversocket,}
31 
32 while True:
33   print "等待活动连接......"
34   #轮询注册的事件集合，返回值为[(文件句柄，对应的事件)，(...),....]
35   events = epoll.poll(timeout)
36   if not events:
37      print "epoll超时无活动连接，重新轮询......"
38      continue
39   print "有" , len(events), "个新事件，开始处理......"
40   
41   for fd, event in events:
42      socket = fd_to_socket[fd]
43      #如果活动socket为当前服务器socket，表示有新连接
44      if socket == serversocket:
45             connection, address = serversocket.accept()
46             print "新连接：" , address
47             #新连接socket设置为非阻塞
48             connection.setblocking(False)
49             #注册新连接fd到待读事件集合
50             epoll.register(connection.fileno(), select.EPOLLIN)
51             #把新连接的文件句柄以及对象保存到字典
52             fd_to_socket[connection.fileno()] = connection
53             #以新连接的对象为键值，值存储在队列中，保存每个连接的信息
54             message_queues[connection]  = Queue.Queue()
55      #关闭事件
56      elif event & select.EPOLLHUP:
57         print 'client close'
58         #在epoll中注销客户端的文件句柄
59         epoll.unregister(fd)
60         #关闭客户端的文件句柄
61         fd_to_socket[fd].close()
62         #在字典中删除与已关闭客户端相关的信息
63         del fd_to_socket[fd]
64      #可读事件
65      elif event & select.EPOLLIN:
66         #接收数据
67         data = socket.recv(1024)
68         if data:
69            print "收到数据：" , data , "客户端：" , socket.getpeername()
70            #将数据放入对应客户端的字典
71            message_queues[socket].put(data)
72            #修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
73            epoll.modify(fd, select.EPOLLOUT)
74      #可写事件
75      elif event & select.EPOLLOUT:
76         try:
77            #从字典中获取对应客户端的信息
78            msg = message_queues[socket].get_nowait()
79         except Queue.Empty:
80            print socket.getpeername() , " queue empty"
81            #修改文件句柄为读事件
82            epoll.modify(fd, select.EPOLLIN)
83         else :
84            print "发送数据：" , data , "客户端：" , socket.getpeername()
85            #发送数据
86            socket.send(msg)
87 
88 #在epoll中注销服务端文件句柄
89 epoll.unregister(serversocket.fileno())
90 #关闭epoll
91 epoll.close()
92 #关闭服务器socket
93 serversocket.close()


 1 #!/usr/bin/env python
 2 #-*- coding:utf-8 -*-
 3 
 4 import socket
 5 
 6 #创建客户端socket对象
 7 clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 8 #服务端IP地址和端口号元组
 9 server_address = ('127.0.0.1',8888)
10 #客户端连接指定的IP地址和端口号
11 clientsocket.connect(server_address)
12 
13 while True:
14     #输入数据
15     data = raw_input('please input:')
16     #客户端发送数据
17     clientsocket.sendall(data)
18     #客户端接收数据
19     server_data = clientsocket.recv(1024)
20     print '客户端收到的数据：'server_data
21     #关闭客户端socket
22     clientsocket.close() 
