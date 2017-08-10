#!/usr/bin/env python
#This is a simple GUI monitor for the bot, it will show the current location on a new gui.
#Run by 'rosrun beginner_tutorials location_monitor_node.py' 
  
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from Tkinter import *
import math
import os
import actionlib 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal



class location:
	def __init__(self, name, inpX,inpY):
		self.name = name
		self.x = inpX
		self.y = inpY

	def getDistance(self,inputX, inputY):
		return math.sqrt(math.pow(inputX-self.x, 2) + math.pow(inputX-self.y, 2))

	def getXYvectorToward(self,currentX,currentY):
		return (self.x - currentX, self.y - currentY)


Locations = [location("Cylinder", -1.5, -3),location("Dumpster",0.5,-3),location("Bookshelf",0,1),location("Barrier",-4.5,1.5)]

client = actionlib.SimpleActionClient('move_base',MoveBaseAction)




root = Tk()
#ROOT is the whole window


leftFrame = Frame(root)
leftFrame.pack(side=LEFT)
#Left Column 
middleFrame = Frame(root)
middleFrame.pack(side=LEFT)
#Middle Column
rightFrame = Frame(root)
rightFrame.pack(side=LEFT)
#Right Column 
def buttonCallBackForTwist():
	print("xxx")

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

global butBool
butBool = False 

def sendGoalAction(index):
	goalLoc = Locations[index]
	print(goalLoc.name)
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id = 'map'
	goal_pose.target_pose.pose.position.x = goalLoc.x
	goal_pose.target_pose.pose.position.y = goalLoc.y
	goal_pose.target_pose.pose.position.z = 0
	goal_pose.target_pose.pose.orientation.x = 0
	goal_pose.target_pose.pose.orientation.y = 0
	goal_pose.target_pose.pose.orientation.z = 1
	goal_pose.target_pose.pose.orientation.w = 0
	client.send_goal(goal_pose)
	client.wait_for_result()
	enableAllLocationButton()

def buttonCallBack1():
	sendGoalAction(0)
	
def buttonCallBack2():
	sendGoalAction(1)

def buttonCallBack3():
	sendGoalAction(2)

def buttonCallBack4():
	sendGoalAction(3)

buttonLoc1 = Button(root,text="GO TO Location 1", fg="black",command=buttonCallBack1)
buttonLoc1.pack()
buttonLoc2 = Button(root,text="GO TO Location 2", fg="black",command=buttonCallBack2)
buttonLoc2.pack()
buttonLoc3 = Button(root,text="GO TO Location 3", fg="black",command=buttonCallBack3)
buttonLoc3.pack()
buttonLoc4 = Button(root,text="GO TO Location 4", fg="black",command=buttonCallBack4)
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
		button5["relief"] = "raised"
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
	x = int(msg.pose.pose.position.x * 100)/100.0
	y = int(msg.pose.pose.position.y * 100)/100.0
	ori_x = msg.pose.pose.orientation.x
	ori_y = msg.pose.pose.orientation.y
	ori_z = msg.pose.pose.orientation.z
	ori_w = msg.pose.pose.orientation.w
	
	locationIndicator['text'] = 'Location:     \nx: {}\ny: {}\n\n'.format(x,y) + 'Orientation:     \nz: {}\nw: {}'.format(int(ori_z*100)/100.0,int(ori_w*100)/100.0)
	
	#rospy.loginfo('location: x:{}, y:{}'.format(x,y))
	#rospy.loginfo('orientation: x:{}, y:{}, z:{},w:{}'.format(ori_x,ori_y,ori_z,ori_w))

def callbackForTwist(msg):
	l_x = int(msg.linear.x * 100)/100.0
	a_z = int(msg.angular.z * 100)/100.0
	
	twistIndicator['text'] = 'Twist:\nLinear(x): {}\nangular(z):{}'.format(l_x,a_z)
	#rospy.loginfo('Function callbackForTwist(msg) Not Implemented Yet.')

def main():
	rospy.init_node('location_monitor')
	rospy.Subscriber("/odom",Odometry,callbackForLocation)
	rospy.Subscriber("/cmd_vel_mux/input/teleop",Twist,callbackForTwist)
	client.wait_for_server()
	root.mainloop()
	
	#rospy.spin()

if __name__ == '__main__':
	main()
	
