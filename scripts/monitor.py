#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry

def callbackLoc(m):
	x = m.pose.pose.position.x
	y = m.pose.pose.position.y
	rospy.loginfo('x: {}, y: {}'.format(x,y))

def main():
	rospy.init_node('monitor')
	
	rospy.Subscriber('/odom',Odometry,callbackLoc)
	rospy.spin()

if __name__ == '__main__':
	main()
