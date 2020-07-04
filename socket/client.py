#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import rospy
import sender
import datetime
from pita_msgs.msg import PoseScan

class RosTopic(object):
    def __init__(self):
        self.sender = sender.RobotSocket()
        self.count = 0

    def recall(self, data):
        self.sender.sendall(1, data.scan.ranges) 

    def listener(self):
        rospy.init_node('listener',  anonymous=True)
        rospy.Subscriber('/lidar/scan_with_pose', PoseScan, self.recall)
        rospy.spin()


if __name__ == "__main__":
    try:
        RosTopic().listener()
    except Exception as e:
        print e
