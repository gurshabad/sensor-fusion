#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
import math

#function to calculate distance in meters from gps lat-long
#Source: http://www.johndcook.com/blog/python_longitude_latitude/
def coordinate_distance(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    return arc * 6373 * 1000

#global variables to store latest gps positions
gps1 = NavSatFix()
gps2 = NavSatFix()

pub = rospy.Publisher('gps_distance', Float64, queue_size=10)

def gpscb2(data):
    global gps1
    gps1 = data

def gpscb1(data):
    global gps2, pub
    gps2 = data
    curr_distance = coordinate_distance(gps1.latitude, gps1.longitude, gps2.latitude, gps2.longitude)
    rospy.loginfo("%f", curr_distance)
    pub.publish(curr_distance)
    
def listener():
    rospy.init_node('gps_listener', anonymous=True)
    rospy.Subscriber("gps1", NavSatFix, gpscb1)
    rospy.Subscriber("gps2", NavSatFix, gpscb2)
    rospy.spin()

if __name__ == '__main__':
    listener()