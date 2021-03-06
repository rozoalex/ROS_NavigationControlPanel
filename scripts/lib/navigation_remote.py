import rospy
import actionlib #For sending action 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
#tf is a lib where you get access to complex math computation 
from tf.msg import tfMessage 
from tf.transformations import quaternion_from_euler #Convert quaternion rotation

#This class keep a list of poses, and gives you a set of easy api to 
#send nav goal to ROS

class destination:
	def __init__(self, name, inpX,inpY,inpZ,inpW):
		self.name = name
		self.x = inpX
		self.y = inpY
		self.z = inpZ #z is part of rotation 
		self.w = inpW #w is part of rotation 

class navigation_remote:
	def __init__(self, destinations):
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		self.Destinations = destinations
	
	def sendGoalAction(index):
		goalLoc = Destinations[index]
		print(goalLoc.name)
		goal_pose = MoveBaseGoal()
		goal_pose.target_pose.header.frame_id = 'map'
		goal_pose.target_pose.pose.position.x = goalLoc.x
		goal_pose.target_pose.pose.position.y = goalLoc.y
		coordinateString = '(x,y)=( {}, {})'.format(
			int(goalLoc.x*100)/100.0,int(goalLoc.y*100)/100.0)
		goal_pose.target_pose.pose.orientation.z = goalLoc.z
		goal_pose.target_pose.pose.orientation.w = goalLoc.w
		rotString = ' (z,w)=( {}, {})'.format(
			int(goalLoc.z*100)/100.0,int(goalLoc.w*100)/100.0)
		infoString = 'Navigation Destination: {}\nGoal Coordinate: {}\nGoal Rotation: {}\n'.format(goalLoc.name,coordinateString,rotString)
		print(infoString)
		navi_info['text'] = infoString + 'Trying...'
		client.send_goal(goal_pose)
		if isSuccessful:#TODO THIS IS NOT RIGHT
			navi_info['text'] = infoString + 'Goal reached!'
		else:
			navi_info['text'] = infoString + 'Failed.'

	
		
		
