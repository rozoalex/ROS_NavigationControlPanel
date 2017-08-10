#include "ros/ros.h"
#include "nav_msgs/Odometry.h"
#include <vector>
#include <string>
#include "beginner_tutorials/LandmarkDistance.h"
#include "math.h"
#include <geometry_msgs/Twist.h> //Twist for controling the robot
#include <stdlib.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
//yoyoyo


using std::vector;
using std::string;
using beginner_tutorials::LandmarkDistance;

//
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
//creates a convenience typedef for a SimpleActionClient
//that will allow us to communicate with actions that adhere to the MoveBaseAction action interface.


class Landmark {
  public:
    Landmark(string name, double x, double y)
      : name(name), x(x), y(y){}
    string name;
    double x;
    double y;

};

class LandmarkMonitor{
  public:  
    //constructor
    LandmarkMonitor(const ros::Publisher& landmark_pub, const ros::Publisher& motion_twist): landmarks_(),landmark_pub_(landmark_pub),motion_twist_(motion_twist){
      InitLandmarks();
    }

    void OdomCallback(const nav_msgs::Odometry::ConstPtr& msg){
      //update the location constantly
      double x = msg->pose.pose.position.x;
      double y = msg->pose.pose.position.y;
      currentLocationX = x;
      currentLocationY = y;
      if(counter%50 == 0){
    	  ROS_INFO("currentLocation x:%f y:%f",x,y);
      }
      counter++;
      //See if we want to do random walk or get goal
      if(doRandomWalk){
        LandmarkDistance ld = FindClosest(x,y);
       // ROS_INFO("x: %s, y: %f", ld.name.c_str(), ld.distance);
        landmark_pub_.publish(ld);
        //publish my message, which indicates what object is closest to the robot
        // Randomly generate a twist and let the robot go with this twist for a random time
        if(ticks == 0){
          base_cmd.linear.x = fRand(-1, 1);
          base_cmd.linear.y = fRand(-1, 1);
          base_cmd.angular.z = fRand(-1, 1);
          ticks = rand() % 100 + 200;
          initTicks = ticks;
          ROS_INFO("Generate new ticks and twist:%d", ticks);//

          ROS_INFO("linear.x:%f linear.y:%f angular.z:%f",base_cmd.linear.x, base_cmd.linear.y, base_cmd.angular.z);
        }else{
          if(ticks % 40 == 1){
            double percentageDone = round(1000.0 * ticks/initTicks)/10 ;
            ROS_INFO("remaining ticks: %d", initTicks);
            ROS_INFO("remaining ticks: %f percent", percentageDone);
          }
          ticks = ticks - 1;
        }
        // Randomly generate a twist and let the robot go with this twist for a random time
        motion_twist_.publish(base_cmd);
        if (ld.distance <= 0.5){
          ROS_INFO("I'm near the %s", ld.name.c_str());
        }
      }else{
        //ROS_INFO("Try to go to Landmark 3");
    	
        //TryGoToLandmarks(6);
        TryGoToLandmarks(4);
      }
    }

    double fRand(double fMin, double fMax){
      double f = (double)rand() / RAND_MAX;
      return fMin + f * (fMax - fMin);
    }

    void TryGoToLandmarks(int index){
      if(!doRandomWalk){
        onMission = true;  
        if(index <= (landmarks_.size()-1)){

          
          const Landmark& landmark = landmarks_[index];
          double currentX = landmark.x;
          double currentY = landmark.y;
          ROS_INFO("Head to %s", landmark.name.c_str());
          //printing some info
          ROS_INFO("target is x:%f y:%f",currentX, currentY);
          //ROS_INFO("Heading to %s", currentName);
          ROS_INFO("I am at x:%f y:%f", currentLocationX, currentLocationY);
          //ROS_INFO("to %s", currentName);
          //printing some info
          
          GoToCoordinate(landmark.x, landmark.y);
          //Do something here
          
        }else{
          int size = landmarks_.size();
          ROS_INFO("Exit there are only %d landmarks pre-saved, your index %d does not exist", size, index);
        }
        //onMission = false;
      }
    }

    private:
      vector<Landmark> landmarks_;
      ros::Publisher landmark_pub_;
      ros::Publisher motion_twist_;
      geometry_msgs::Twist base_cmd;
      bool doRandomWalk;
      bool onMission;
      int ticks;
      int initTicks;
      double currentLocationX;
      double currentLocationY;
      int counter;

      //hard-code the locations of the objects on the map
      void InitLandmarks(){
    	counter = 0;
        doRandomWalk = false;
        onMission = false;
        ticks = 0;
        initTicks = 0;
        currentLocationX = 0;
        currentLocationY = 0;
        landmarks_.push_back(Landmark("Cube", 1.43, -1.03));//0
        landmarks_.push_back(Landmark("Dumpster", 1, -3.44));//1
        landmarks_.push_back(Landmark("Cylinder", -2, -3.5));
        landmarks_.push_back(Landmark("Barrier", -4, -1));
        landmarks_.push_back(Landmark("Bookshelf", 0, 1.53));
        landmarks_.push_back(Landmark("Orgin", 0, 0));//5
        landmarks_.push_back(Landmark("x=1 y=0", 1, 0));
        landmarks_.push_back(Landmark("x=0 y=1", 0, 1));//7
      }



      void GoToCoordinate(double target_x, double target_y){
        //NAV GOAL CODE
        //NAV GOAL CODE
        double current_x = currentLocationX;
        double current_y = currentLocationY;
        MoveBaseClient ac("move_base", true);
        //tell the action client that we want to spin a thread by default
        while(!ac.waitForServer(ros::Duration(5.0))){
          ROS_INFO("Waiting for the move_base action server to come up");
        }
        //wait for the action server to come up

        move_base_msgs::MoveBaseGoal goal;

        goal.target_pose.header.frame_id = "base_link";
        goal.target_pose.header.stamp = ros::Time::now();

        goal.target_pose.pose.position.x = target_x - current_x;
        goal.target_pose.pose.position.y = target_y - current_y;
        goal.target_pose.pose.orientation.w = 1.0;

        ROS_INFO("Sending nav goal... I am at x: %f y: %f", current_x, current_y);
        ROS_INFO("Try to go to x: %f y: %f", target_x, target_y);
        ac.sendGoal(goal);

        ac.waitForResult();

        if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
          ROS_INFO("Hooray, delivered :)");
          
        else
          ROS_INFO("Nah, failed :(");
        
        ROS_INFO("I am at x: %f y: %f", currentLocationX, currentLocationY);
        ROS_INFO("Goal was position.x:%f position.y:%f orientation.w:%f",goal.target_pose.pose.position.x, goal.target_pose.pose.position.y, goal.target_pose.pose.orientation.w);
        
      }

      //find the closest object in the map
      LandmarkDistance FindClosest(double x, double y){
        LandmarkDistance result;
        result.distance = -1;
        for(size_t i = 0; i <landmarks_.size(); ++i){
          const Landmark& landmark = landmarks_[i];
          double xd = landmark.x - x;
          double yd = landmark.y - y;
          double distance = sqrt(xd*xd + yd*yd);

          if (result.distance < 0 || distance < result.distance){
            result.name = landmark.name;
            result.distance = distance;
          }
        }
        return result;
      }


};

//The main
int main(int argc, char** argv){
  ros::init(argc, argv, "location_monitor");
  ros::NodeHandle nh;
  ros::Publisher landmark_pub = nh.advertise<LandmarkDistance>("closest_landmark",10); //closest_landmark publisher
  ros::Publisher motion_twist = nh.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/teleop", 1);//twist publisher
  LandmarkMonitor monitor(landmark_pub, motion_twist); //init a LandmarkMonitor Instance with the two publisher

  ros::Subscriber sub = nh.subscribe("odom",10,&LandmarkMonitor::OdomCallback, &monitor);
  //subscribe the odom with OdomCallback function in LandmarkMonitor, and give it an instance of that

  //NAV GOAL CODE
  //NAV GOAL CODE
  MoveBaseClient ac("move_base", true);
  //tell the action client that we want to spin a thread by default
  while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
    ROS_INFO("Oh, come on..... Really?");
  }
  //wait for the action server to come up

  move_base_msgs::MoveBaseGoal goal;

  goal.target_pose.header.frame_id = "base_link";
  goal.target_pose.header.stamp = ros::Time::now();

  goal.target_pose.pose.position.x = 1.0;
  goal.target_pose.pose.orientation.w = 1.0;

  ROS_INFO("Sending nav goal...");
  ac.sendGoal(goal);

  ac.waitForResult();

  if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED){
    ROS_INFO("Hooray, delivered :)");
    ROS_INFO("position.x:%f position.y:%f orientation.w:%f",goal.target_pose.pose.position.x, goal.target_pose.pose.position.y, goal.target_pose.pose.orientation.w);
  }else{
    ROS_INFO("Nah, failed :(");
  }
  //NAV GOAL CODE
  //NAV GOAL CODE

  ros::spin();

  return 0;
}
