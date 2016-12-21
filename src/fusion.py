#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import math

#normal distributions defined as: [mean, standard deviation]
#sums are additional values helping us compute the values on the fly
#sums defined as: [num of values, sum of values, sum of square of values]
gps_distribution = [0.0, 0.0]
gps_sums = [0.0, 0.0, 0.0]
lidar_distribution = [0.0, 0.0]
lidar_sums = [0.0, 0.0, 0.0]
last_gps_reading = 0.0
last_lidar_reading = 0.0

def lidar_d(msg):
	global last_lidar_reading, last_gps_reading
	last_lidar_reading = msg.data

	global lidar_sums
	#update sums
	lidar_sums[0] += 1
	lidar_sums[1] += msg.data
	lidar_sums[2] += msg.data*msg.data

	global lidar_distribution
	#update distribution
	lidar_distribution[0] = lidar_sums[1]/float(lidar_sums[0])
	lidar_distribution[1] = math.sqrt((lidar_sums[0] * lidar_sums[2] - lidar_sums[1] * lidar_sums[1])/float(lidar_sums[0] * (lidar_sums[0] - 1)))

	#calculate best estimate
	new_mean = (lidar_distribution[0]*(gps_distribution[1]**2) + gps_distribution[0]*(lidar_distribution[1]**2))/(lidar_distribution[1]**2 + gps_distribution[1]**2)
	rospy.loginfo("GPS: %f, LIDAR: %f, EST: %f", gps_distribution[0], lidar_distribution[0], new_mean)
	#rospy.loginfo(new_mean)

def gps_d(msg):
	global last_gps_reading, last_lidar_reading
	last_gps_reading = msg.data

	global gps_sums
	#update sums
	gps_sums[0] += 1
	gps_sums[1] += msg.data
	gps_sums[2] += msg.data*msg.data

	global gps_distribution
	#update distribution
	gps_distribution[0] = gps_sums[1]/float(gps_sums[0])
	gps_distribution[1] = math.sqrt((gps_sums[0] * gps_sums[2] - gps_sums[1] * gps_sums[1])/float(gps_sums[0] * (gps_sums[0] - 1)))

	#rospy.loginfo("%f, %f", gps_distribution[0], gps_distribution[1])
    
def listener():
    rospy.init_node('fusion_node', anonymous=True)
    rospy.Subscriber("lidar_distance", Float64, lidar_d)
    rospy.Subscriber("gps_distance", Float64, gps_d)
    rospy.spin()

if __name__ == '__main__':
    listener()