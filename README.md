# sensor-fusion
A generic module for fusing the same information obtained from two sensors, with an example of fusing GPS and LIDAR readings.

# temp
rosbag play 2016-12-14-17-25-07.bag /mavros/global_position/global:=gps1 /velodyne_points:=lidar1

rosbag play 2016-12-14-17-28-30.bag /mavros/global_position/global:=gps2
