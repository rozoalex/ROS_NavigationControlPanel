import lib.controller_ui_module
import lib.navigation_remote
import rospy
#chmod +x location_remote_node.py
###
# $ roslaunch turtlebot_gazebo turtlebot_world.launch
# $ roslaunch turtlebot_rviz_launchers view_navigation.launch
# $ roslaunch turtlebot_gazebo amcl_demo.launch

def main():
	print("sss")
	#rospy.init_node('location_remote')#tell ROS to init this node
	#ui = controller_ui_module() #init the ui
	#destinations = []
	#destinations = [destination("Cylinder", -1.22, -2.32,0.4578,0.889),
	#	destination("Dumpster",0.6913,-2.066,0.891,0.455),
	#	destination("Bookshelf",0.2047,1.22,-0.7596,0.6504),
	#	destination("Barrier",-3.8,0.2715,0,1)]

	#destinations = [destination("Kitchen", 0.59, -2.05,0.969, -0.247),
	#	destination("TV",2.06,3.84,0.908,-0.42),
	#	destination("Desk",-0.22,0.198,-0.0345,1),
	#	destination("Dinning",-3.8,0.2715,0,1)]
	#remote = navigation_remote(destinations)
	#ui.spin()

if __name__ == '__main__':
	main()
