# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from multiprocessing import Queue
from multiprocessing import Process

msg_que = Queue()


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def timer_process(que):
    current_time = time.time()
    while 1:
        if time.time() - current_time > 3:
            current_time = time.time()
            try:
                que.put(get_current_time())
            except Exception, put_error:
                print '[%s] error info: %s' % (get_current_time(), put_error)
        else:
            pass


def event_process(que):
    while 1:
        if not que.empty():
            print '[%s] que get' % get_current_time()
            try:
                msg = que.get()
                print '[%s] get content is %s' % (get_current_time(), msg)
            except Exception, get_error:
                print '[%s] error info: %s' % (get_current_time(), get_error)


if __name__ == "__main__":
    timer_pro = Process(target=timer_process, args=(msg_que,))
    event_pro = Process(target=event_process, args=(msg_que,))

    timer_pro.start()
    print 'timer start'

    event_pro.start()
    print 'event start'
