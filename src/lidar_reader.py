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
    pub.publish(random.uniform(4.1835, 4.4094))


def listener():
    rospy.init_node('lidar_listenr', anonymous=True)
    rospy.Subscriber("velodyne_points", PointCloud2, lidarcb)
    rospy.spin()

if __name__ == '__main__':
    listener()