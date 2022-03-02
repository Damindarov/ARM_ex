// *** include ***
#include <cmath>
#include <functional>
#include <ros/ros.h>
#include "std_msgs/String.h"
#include <sstream>

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
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Bool.h>


std::vector<float> desired_pose = {0, 0, 0, 0};
std::vector<float> joint_desired_pose = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // q1,q3,q4 from arm to ste same kuka
std::vector<float> desired_posekuka = {0, 0, 0, 0};


// void waitForMotion(iiwa_ros::service::TimeToDestinationService& time_2_dist, double time_out = 2.0)
// {
//     double time = time_2_dist.getTimeToDestination();
//     ros::Time start_wait = ros::Time::now();
//     while (time < 0.0 && (ros::Time::now() - start_wait) < ros::Duration(time_out)) {
//         ros::Duration(0.5).sleep();
//         time = time_2_dist.getTimeToDestination();
//     }
//     if (time > 0.0) {
//         // ROS_INFO_STREAM("Sleeping for " << time << " seconds.");
//         ros::Duration(time).sleep();
//     }
// }

void pose_callback(std_msgs::Float32MultiArray msg)
{
    // if (fabs(desired_pose[0]-msg.data[0]) > 0.02 && fabs(desired_pose[1]-msg.data[1]) > 0.02 && fabs(desired_pose[2]-msg.data[2]) > 0.02 )
    {
        joint_desired_pose[0] = msg.data[0];
        joint_desired_pose[1] = msg.data[1];
        joint_desired_pose[2] = msg.data[2];
        joint_desired_pose[3] = msg.data[3];
        joint_desired_pose[4] = msg.data[4];
        joint_desired_pose[5] = msg.data[5];

        joint_desired_pose[6] = msg.data[6];
        joint_desired_pose[7] = msg.data[7];
        joint_desired_pose[8] = msg.data[8];
        joint_desired_pose[9] = msg.data[9];
        joint_desired_pose[10] = msg.data[10];
        joint_desired_pose[11] = msg.data[11];
        
    }
    // else
    // {
    //     desired_pose = {0, 0, 0};
    // }
}

// void chatterCallback_Kuka(const std_msgs::Float32MultiArray::ConstPtr& msg)
// {
//     ROS_INFO("I heard: [%f],[%f],[%f],[%f]", msg->data.at(0),msg->data.at(1),msg->data.at(2),msg->data.at(3));
//     desired_posekuka[0] = msg.data[0];
//     desired_posekuka[1] = msg.data[1];
//     desired_posekuka[2] = msg.data[2];
// }s

int main(int argc, char **argv)
{

    ros::init(argc, argv, "tele_iiwa");
    ros::NodeHandle nh;
    // ros spinner
    ros::AsyncSpinner spinner(1);
    spinner.start();
    // Wait a bit, so that you can be sure the subscribers are connected.
    ros::Duration(0.05).sleep();

    // *** decleare ***
    // services
    iiwa_ros::service::ControlModeService control_mode;
    iiwa_ros::service::PathParametersService j_vel;

    iiwa_ros::service::PathParametersLinService c_vel;
    iiwa_ros::service::TimeToDestinationService time_to_dist;
    // commands
    iiwa_ros::command::CartesianPose cp_command;
    iiwa_ros::command::CartesianPoseLinear cpl_command;
    iiwa_ros::command::JointPosition jp_command;
    iiwa_ros::command::JointVelocity jv_command;
    // states
    iiwa_ros::state::CartesianWrench cw_state;
    iiwa_ros::state::CartesianPose cp_state;
    iiwa_ros::state::JointVelocity jv_state;
    iiwa_ros::state::JointPosition jp_state;
    iiwa_ros::state::ExternalJointTorque exjt_state;
    // cartesian position msg
    geometry_msgs::PoseStamped init_pos, new_pose;
    // cartesian velocity msg
    geometry_msgs::Twist cartesian_velocity;

    double vel = 0.75;
    double Jvel = 0.15;
    cartesian_velocity.linear.x = vel;
    cartesian_velocity.linear.y = vel;
    cartesian_velocity.linear.z = vel;
    cartesian_velocity.angular.x = vel;
    cartesian_velocity.angular.y = vel;
    cartesian_velocity.angular.z = vel;
    ros::Subscriber sub = nh.subscribe("/lefttop_point", 1000, pose_callback);
    ros::spinOnce();
    // *** initialize ***
    // services
    control_mode.init("iiwa");
    j_vel.init("iiwa");
    c_vel.init("iiwa");
    time_to_dist.init("iiwa");
    // commands
    cp_command.init("iiwa");
    cpl_command.init("iiwa");
    jp_command.init("iiwa");
    jv_command.init("iiwa");
    // states
    cw_state.init("iiwa");
    cp_state.init("iiwa");
    jv_state.init("iiwa");
    jp_state.init("iiwa");
    exjt_state.init("iiwa");


    ros::Publisher chatter_pub = nh.advertise<std_msgs::Float32MultiArray>("Coordinate_public", 1000);
    // ros::Publisher gripper_command = nh.advertise<std_msgs::Bool>("/iiwa/command/GripperCommand", 1000);

    // gripper
    std_msgs::Bool gripper;
    bool open = true;
    bool close = false;
    bool station = true;
    gripper.data = open;
    // gripper_command.publish(gripper);

    // set the cartesian and joints velocity limit
    c_vel.setMaxCartesianVelocity(cartesian_velocity);
    j_vel.setSmartServoJointSpeedLimits(1.0, 0.75);
    ros::Duration(0.1).sleep(); // wait to initialize ros topics
    // std::vector<float> orient = {0.707165002823, 0.707041292473, -0.00230447391603, -0.00221763853181};
    while (true)
    {
        auto cartesian_position = cp_state.getPose();
        auto joint_position = jp_state.getPosition();
        auto force = exjt_state.getTorque();
        std_msgs::Float32MultiArray msg;

        msg.data = {joint_position.position.a1, joint_position.position.a2,
                    joint_position.position.a3, joint_position.position.a4, joint_position.position.a5,
                    joint_position.position.a6, joint_position.position.a7};
        // std::cout << msg << std::endl;
//        ROS_INFO("%s\n\n", msg.data.c_str());

        chatter_pub.publish(msg);
        joint_position.position.a1 = joint_desired_pose[0]*0.8;
        
        joint_position.position.a2 = (joint_desired_pose[1] + 3.14/4)*0.8;
        joint_position.position.a4 = (-joint_desired_pose[2] - 3.14/2 - 3.14/4)*0.8;
        // if(joint_position.position.a4 < -1.7){
        //     joint_position.position.a4 = -1.7;
        // }
        joint_position.position.a5 = (joint_desired_pose[3]-0.7)*0.8;

        // joint_position.position.a6 = (joint_desired_pose[4] * 2.65);
        // if(abs(joint_position.position.a6) < 0.1){
        //     joint_position.position.a6 = 0;
        // }
        jp_command.setPosition(joint_position);


        // if(abs(joint_desired_pose[5]) > 1.00 and station){
        //     gripper.data = close;
        //     gripper_command.publish(gripper);
        //     ros::Duration(0.2).sleep();
        //     station = false;

        // }
        // if(abs(joint_desired_pose[5]) < 1.00 and !station){
        //     gripper.data = open;
        //     gripper_command.publish(gripper);
        //     ros::Duration(0.2).sleep();
        //     station = true;
        

        // }
        if (fabs(joint_desired_pose[0] - joint_position.position.a4) > 0 or
            fabs(joint_desired_pose[1] - joint_position.position.a1) > 0 or
            fabs(joint_desired_pose[2] - joint_position.position.a6) > 0)
        {
            // joint_position.position.a1 = joint_desired_pose[1];
            // joint_position.position.a6 = joint_desired_pose[2];
            // joint_position.position.a4 = -3.14/2 - joint_desired_pose[0];
            // init_pos.pose.position.x = desired_pose[0];
            // init_pos.pose.position.y = desired_pose[1];
            // init_pos.pose.position.z = desired_pose[2];
            // jp_command.setPosition(joint_position);
                std::cout<<std::to_string(joint_desired_pose[0])<<", "<<std::to_string(joint_desired_pose[1])<<", "<<std::to_string(joint_position.position.a4)<<", "<<std::to_string(joint_desired_pose[3])<<std::endl;
        }
    }
}
