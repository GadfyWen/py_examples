#!/usr/bin/python
#-*-coding:utf-8-*-

import redis


import time
 
number_list = ['300033', '300032', '300031', '300030']
signal = ['1', '-1', '1', '-1']
 
rc = redis.StrictRedis(host='localhost', port='6379')
for i in range(len(number_list)):
    value_new = str(number_list[i]) + ' ' + str(signal[i])
    rc.publish("test", value_new)

