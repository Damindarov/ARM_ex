// *** include ***
#include <cmath>
#include <functional>
#include <ros/ros.h>
#include "std_msgs/String.h"
#include <sstream>
#include <fstream>
#include <ctime>
#include <sys/time.h>
#include <chrono>

// services
#include <iiwa_ros/service/control_mode.hpp>
#include <iiwa_ros/service/path_parameters.hpp>
#include <iiwa_ros/service/path_parameters_lin.hpp>
#include <iiwa_ros/service/time_to_destination.hpp>
// commands
#include <iiwa_ros/command/cartesian_pose.hpp>
#include <iiwa_ros/command/cartesian_pose_linear.hpp>
#include <iiwa_ros/command/joint_position.hpp>
#include <iiwa_ros/command/joint_velocity.hpp>
// states
#include <iiwa_ros/state/cartesian_wrench.hpp>
#include <iiwa_ros/state/cartesian_pose.hpp>
#include <iiwa_ros/state/joint_velocity.hpp>
#include <iiwa_ros/state/joint_position.hpp>
#include <iiwa_ros/state/external_joint_torque.hpp>
// conversions functions hpp_file
#include <iiwa_ros/conversions.hpp>
// messages
#include <iiwa_msgs/DOF.h>
#include <iiwa_msgs/CartesianQuantity.h>
#include <iiwa_msgs/JointPosition.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Bool.h>
int skipper = -100000;

using namespace std::chrono;

void pose_callback(iiwa_msgs::JointPosition msg)
{
    std::cout<<msg.position.a1<<std::endl;
    
    time_t curr_time;
    curr_time = time(NULL);
    nanoseconds ns = duration_cast< nanoseconds >(system_clock::now().time_since_epoch());

    time_t mnow = curr_time;


    std::fstream fs;
    fs.open ("New_points_Kuka.txt", std::fstream::in | std::fstream::out | std::fstream::app);

    fs<<"Time  ";
    fs<< std::to_string(ns.count());
    fs<<", ";
    fs<<std::to_string(msg.position.a1);
    fs<<", ";
    fs<<std::to_string(msg.position.a2);
    fs<<", ";
    fs<<std::to_string(msg.position.a3);
    fs<<", ";
    fs<<std::to_string(msg.position.a4);
    fs<<", ";
    fs<<std::to_string(msg.position.a5);
    fs<<", ";
    fs<<std::to_string(msg.position.a6);
    fs<<", ";
    fs<<std::to_string(msg.position.a7);
    fs<<", ";
    fs<<'\n';
    fs.close();

}


int main(int argc, char **argv)
{
    ros::init(argc,argv,"iiwa_ros1");
    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe("/iiwa/state/JointPosition",1000,pose_callback);
    ros::spin();
}
