# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from multiprocessing import Event
from multiprocessing import Process

event = Event()


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def timer_event(e):
    while 1:
        time.sleep(3)
        e.set()
        print 'count'


def do_event(e):
    while 1:
        e.wait()
        print '[%s] event comes' % get_current_time()
        e.clear()

if __name__ == '__main__':
    timer_pro = Process(target=timer_event, args=(event,))
    do_pro = Process(target=do_event, args=(event,))


    timer_pro.start()
    print timer_pro.name
    do_pro.start()
    print do_pro.name

    print 'pros have been started'
