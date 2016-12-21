#!/usr/bin/env python
import rospy
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Float64
import random
import array 
pub = rospy.Publisher('lidar_distance', Float64, queue_size=10)

def lidarcb(msg):
    global pub
    lst = list(array.array("B", msg.data))


def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber("velodyne_points", PointCloud2, lidarcb)
    rospy.spin()

if __name__ == '__main__':
    listener()