#!/usr/bin/python
#-*-coding:utf-8-*-

import pika
import time

"""
"""

class QueHub(object):
    def __init__(self, queue_name="hello"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)

    def msg_pub(self, msg):
        print "connection open: ", self.connection.is_open
        print "channel open: ", self.channel.is_open
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=msg) 

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    sender = QueHub()
    sender.msg_pub(str(time.time())) 
