#!/usr/bin/env python
#This is a simple and ugly GUI monitor for the bot, it will show the current location on a new gui.
#IMPORTANT
#Due to the runtime dependency, you have to do a serie of commands 
#before run this script.
#The following commands is not the only possibility
#Just for you to quickly set it up
#It will open the gazebo default map and use that
#DO NOT TELEOP, it will interfer the navigation service
###
# $ roslaunch turtlebot_gazebo turtlebot_world.launch
# $ roslaunch turtlebot_rviz_launchers view_navigation.launch
# $ roslaunch turtlebot_gazebo amcl_demo.launch
#then run this script
# $ rosrun beginner_tutorials location_monitor_node.py 
import lib.controller_ui_module
import lib.navigation_remote
import rospy
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Transform
from tf2_msgs.msg import TFMessage
from Tkinter import * #Python ui lib
import math
import os #For calling system command 
import actionlib #For sending action 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
#tf is a lib where you get access to complex math computation 
from tf.msg import tfMessage 
from tf.transformations import quaternion_from_euler #Convert quaternion rotation


class location:
	def __init__(self, name, inpX,inpY,inpZ,inpW):
		self.name = name
		self.x = inpX
		self.y = inpY
		self.z = inpZ #z is part of rotation 
		self.w = inpW #w is part of rotation 

	def getDistance(self,inputX, inputY):
		return math.sqrt(math.pow(inputX-self.x, 2) + math.pow(inputX-self.y, 2))

	def getXYvectorToward(self,currentX,currentY):
		return (self.x - currentX, self.y - currentY)

#This class is for managing ui

	

class CurrentState:
	def __init__(self, x, y):
		self.current_x = x
		self.current_y = y


#Locations = [location("Cylinder", -1.22, -2.32,0.4578,0.889),location("Dumpster",0.6913,-2.066,0.891,0.455),location("Bookshelf",0.2047,1.22,-0.7596,0.6504),location("Barrier",-3.8,0.2715,0,1)]

Locations = [location("Kitchen", 0.59, -2.05,0.969, -0.247),location("TV",2.06,3.84,0.908,-0.42),location("Desk",-0.22,0.198,-0.0345,1),location("Dinning",-3.8,0.2715,0,1)]


#Hardcode with location=(x,y) and rotation = (z,w)

client = actionlib.SimpleActionClient('move_base',MoveBaseAction)


current_AMCL_pose = PoseWithCovarianceStamped() 
current_Odom_pose = Odometry()
current_state = CurrentState(0,0)
#record what amcl is posting 
#A estimation of the current pose


root = Tk()
#ROOT is the whole window
topFrame = Frame(root)
topFrame.pack(side=TOP)
downFrame = Frame(root)
downFrame.pack(side=BOTTOM)
#Down Row for info about navigation
leftFrame = Frame(topFrame)
leftFrame.pack(side=LEFT)
#Left Column for info about the current location
middleFrame = Frame(topFrame)
middleFrame.pack(side=LEFT)
#Middle Column for a controller to be implemented with twist
rightFrame = Frame(topFrame)
rightFrame.pack(side=LEFT)
#Right Column for Adding nav goal

##TODO
def buttonCallBackForTwist():
	print("nah, you haven't implemented this yet")
##TODO
#DOWN
navi_info = Label(downFrame, text="No Navigation Started.", font=("Helvetica", 16),anchor=W, justify=LEFT)#
navi_info.pack()
#DOWN
#LEFT
locationIndicator = Label(leftFrame, text="location: x:--\ny:--\norientation: z: --\nw: --", font=("Helvetica", 16),anchor=W, justify=LEFT)#Show Location
twistIndicator = Label(leftFrame, text="-", font=("Helvetica", 16),anchor=W, justify=LEFT)#Show twist
locationIndicator.pack()
twistIndicator.pack(side=BOTTOM)
#LEFT
#MID
midUpFrame=Frame(middleFrame)
midUpFrame.pack(side=TOP)
midMidFrame=Frame(middleFrame)
midMidFrame.pack(side=TOP)
midBotFrame=Frame(middleFrame)
midBotFrame.pack(side=TOP)
#
button1 = Button(midUpFrame,text="", fg="red",command=buttonCallBackForTwist)
button1.pack(side=LEFT)
button2 = Button(midUpFrame,text="^", fg="red",command=buttonCallBackForTwist)
button2.pack(side=LEFT)
button3 = Button(midUpFrame,text="", fg="red",command=buttonCallBackForTwist)
button3.pack(side=LEFT)
#
button4 = Button(midMidFrame,text="<", fg="red",command=buttonCallBackForTwist)
button4.pack(side=LEFT)
button5 = Button(midMidFrame,text="x", fg="red",command=buttonCallBackForTwist)
button5.pack(side=LEFT)
button6 = Button(midMidFrame,text=">", fg="red",command=buttonCallBackForTwist)
button6.pack(side=LEFT)
#
button7 = Button(midBotFrame,text="", fg="red",command=buttonCallBackForTwist)
button7.pack(side=LEFT)
button8 = Button(midBotFrame,text="v", fg="red",command=buttonCallBackForTwist)
button8.pack(side=LEFT)
button9 = Button(midBotFrame,text="", fg="red",command=buttonCallBackForTwist)
button9.pack(side=LEFT)
#

#MID


#where a goal destination is send to the navigation stack,
#The robot should try to go there
def sendGoalAction(index):
	goalLoc = Locations[index]
	print(goalLoc.name)
	#current_x= current_AMCL_pose.pose.pose.position.x
	#current_y= current_AMCL_pose.pose.pose.position.y
	#current_x= current_Odom_pose.pose.pose.position.x
	#current_y= current_Odom_pose.pose.pose.position.y
	#new_yaw = math.atan((goalLoc.x - current_state.current_x)/(goalLoc.y - current_state.current_y))
	#print(new_yaw)
	#print(current_state.current_x)
	#print(current_state.current_y)
	#p = quaternion_from_euler(0, 0, new_yaw)
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id = 'map'
	goal_pose.target_pose.pose.position.x = goalLoc.x
	goal_pose.target_pose.pose.position.y = goalLoc.y
	coordinateString = '(x,y)=( {}, {})'.format(int(goalLoc.x*100)/100.0,int(goalLoc.y*100)/100.0)
	goal_pose.target_pose.pose.orientation.z = goalLoc.z
	goal_pose.target_pose.pose.orientation.w = goalLoc.w
	rotString = ' (z,w)=( {}, {})'.format(int(goalLoc.z*100)/100.0,int(goalLoc.w*100)/100.0)
	infoString = 'Navigation Destination: {}\nGoal Coordinate: {}\nGoal Rotation: {}\n'.format(goalLoc.name,coordinateString,rotString)
	print(infoString)
	navi_info['text'] = infoString + 'Trying...'
	root.update()
	client.send_goal(goal_pose)
	isSuccessful =client.wait_for_result()
	if isSuccessful:
		navi_info['text'] = infoString + 'Goal reached!'
	else:
		navi_info['text'] = infoString + 'Failed.'
	goal_pose.target_pose.pose.position.x = goalLoc.x
	goal_pose.target_pose.pose.position.y = goalLoc.y
	##
	#ROS uses Quaternion rotation, 
	#(x,y,z,w)=(0,0,0,1) means no rotation
	#Use quaternion_from_euler(roll, pitch, yaw) 
	#to convert RPY to Quaternion 
	#Doc:http://wiki.ros.org/Tutorials/Quaternions
	##
	enableAllLocationButton() #DONT forget to set free all buttons

def buttonCallBack1():
	sendGoalAction(0)
	
def buttonCallBack2():
	sendGoalAction(1)

def buttonCallBack3():
	sendGoalAction(2)

def buttonCallBack4():
	sendGoalAction(3)

buttonLoc1 = Button(rightFrame,text="GO TO Location 1", fg="black",command=buttonCallBack1)
buttonLoc1.pack()
buttonLoc2 = Button(rightFrame,text="GO TO Location 2", fg="black",command=buttonCallBack2)
buttonLoc2.pack()
buttonLoc3 = Button(rightFrame,text="GO TO Location 3", fg="black",command=buttonCallBack3)
buttonLoc3.pack()
buttonLoc4 = Button(rightFrame,text="GO TO Location 4", fg="black",command=buttonCallBack4)
buttonLoc4.pack()

def disableAllLocationButton():
	buttonLoc1["state"] = 'disable'
	buttonLoc2["state"] = 'disable'
	buttonLoc3["state"] = 'disable'
	buttonLoc4["state"] = 'disable'

def enableAllLocationButton():
	buttonLoc1["state"] = 'normal'
	buttonLoc2["state"] = 'normal'
	buttonLoc3["state"] = 'normal'
	buttonLoc4["state"] = 'normal'

def keyPressed(event):
	print "pressed", repr(event.char)
	if event.char == "w":
		disableAllLocationButton()
		button2["relief"] = "sunken"
		button2.invoke()
		button2["state"] = 'disable'
	elif event.char == "a":
		disableAllLocationButton()
		button4["relief"] = "sunken"
		button4.invoke()
		button4["state"] = 'disable'
	elif event.char == "s":
		disableAllLocationButton()
		button5["relief"] = "sunken"
		button5.invoke()
		button5["state"] = 'disable'
	elif event.char == "d":
		disableAllLocationButton()
		button6["relief"] = "sunken"
		button6.invoke()
		button6["state"] = 'disable'
	elif event.char == "x":
		disableAllLocationButton()
		button8["relief"] = "sunken"
		button8.invoke()
		button8["state"] = 'disable'
	elif event.char == "1":
		if buttonLoc1["state"] != 'disable':
			buttonLoc1["relief"] = "sunken"
			buttonLoc1.invoke()
			disableAllLocationButton()
	elif event.char == "2":
		if buttonLoc2["state"] == 'disable':
			buttonLoc2["relief"] = "sunken"
			buttonLoc2.invoke()
			disableAllLocationButton()
	elif event.char == "3":
		if buttonLoc3["state"] == 'disable':
			buttonLoc3["relief"] = "sunken"
			buttonLoc3.invoke()
			disableAllLocationButton()
	elif event.char == "4":
		if buttonLoc4["state"] == 'disable':
			buttonLoc4["relief"] = "sunken"
			buttonLoc4.invoke()
			disableAllLocationButton()
	elif event.char == "\x1b":
		root.destroy()
		print("Exit.")

def keyReleased(event):
	print "released", repr(event.char)
	if event.char == "w":
		button2["relief"] = "raised"
		button2["state"] = 'normal'
	elif event.char == "a":
		button4["relief"] = "raised"
		button4["state"] = 'normal'
	elif event.char == "s":
		button5["reuch harder for gmapplief"] = "raised"
		button5["state"] = 'normal'
	elif event.char == "d":
		button6["relief"] = "raised"
		button6["state"] = 'normal'
	elif event.char == "x":
		button8["relief"] = "raised"
		button8["state"] = 'normal'


root.bind("<Key>", keyPressed)
root.bind('<KeyRelease>',keyReleased)

def callbackForLocation(msg):
	#print("callBackForLocation")
	current_Odom_pose = msg
	current_state.current_x = int(msg.pose.pose.position.x * 100)/100.0
	current_state.current_y = int(msg.pose.pose.position.y * 100)/100.0
	ori_x = msg.pose.pose.orientation.x
	ori_y = msg.pose.pose.orientation.y
	ori_z = msg.pose.pose.orientation.z
	ori_w = msg.pose.pose.orientation.w
	
	locationIndicator['text'] = 'Location:     \nx: {}\ny: {}\n\n'.format(current_state.current_x,current_state.current_y) + 'Orientation:     \nz: {}\nw: {}'.format(int(ori_z*100)/100.0,int(ori_w*100)/100.0)
	
	#rospy.loginfo('location: x:{}, y:{}'.format(x,y))
	#rospy.loginfo('orientation: x:{}, y:{}, z:{},w:{}'.format(ori_x,ori_y,ori_z,ori_w))

#def callbackForLocFromAMCL(msg):
#	current_AMCL_pose = msg

def callbackForTf(msg):
	#update the current location reading 
	current_state.current_x = msg.transforms[0].transform.translation.x
	current_state.current_y = msg.transforms[0].transform.translation.y
	ori_z = msg.transforms[0].transform.rotation.z
	ori_w = msg.transforms[0].transform.rotation.w
	print(msg.transforms)
	print("----------\n----------\n----------\n")
	locationIndicator['text'] = 'Location:     \nx: {}\ny: {}\n\n'.format(int(current_state.current_x * 100)/100.0,int(current_state.current_y * 100)/100.0) + 'Orientation:     \nz: {}\nw: {}'.format(int(ori_z*100)/100.0,int(ori_w*100)/100.0)

def callbackForTwist(msg):
	l_x = int(msg.linear.x * 100)/100.0
	a_z = int(msg.angular.z * 100)/100.0
	
	twistIndicator['text'] = 'Twist:\nLinear(x): {}\nangular(z):{}'.format(l_x,a_z)

def main():
	rospy.init_node('location_monitor')
	rospy.Subscriber("/odom",Odometry,callbackForLocation)
	rospy.Subscriber("/cmd_vel_mux/input/teleop",Twist,callbackForTwist)
	#rospy.Subscriber("amcl_pose",PoseWithCovarianceStamped,callbackForLocFromAMCL)
	#rospy.Subscriber("/tf",TFMessage,callbackForTf)
	client.wait_for_server()
	root.mainloop()

	
	#rospy.spin()

if __name__ == '__main__':
	main()
	
