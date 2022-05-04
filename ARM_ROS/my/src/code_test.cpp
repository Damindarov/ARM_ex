// *** include ***
#include <cmath>
#include <functional>
#include <ros/ros.h>
#include "std_msgs/String.h"
#include "std_msgs/Float32MultiArray.h"
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
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Bool.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <iostream>
#include <cstring>
#include<thread>

std::vector<float> desired_pose = {0, 0, 0, 0};
std::vector<float> joint_desired_pose = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // q1,q3,q4 from arm to ste same kuka
std::vector<float> desired_posekuka = {0, 0, 0, 0};

using namespace std::chrono;

void pose_callback(std_msgs::Float32MultiArray msg)
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
        time_t curr_time;
        curr_time = time(NULL);
        nanoseconds ns = duration_cast< nanoseconds >(system_clock::now().time_since_epoch());
        time_t mnow = curr_time;
        std::fstream fs;
        fs.open ("datas_iiwa2_listener.txt", std::fstream::in | std::fstream::out | std::fstream::app);
        fs<<"Time  ";
        fs<< std::to_string((ns).count());
        fs<<", ";
        fs<<std::to_string(joint_desired_pose[5]);
        fs<<", ";
        fs<<std::to_string(joint_desired_pose[6]);
        fs<<", ";
        fs<<std::to_string(0);
        fs<<", ";
        fs<<std::to_string(joint_desired_pose[7]);
        fs<<", ";
        fs<<std::to_string(joint_desired_pose[8]);
        fs<<", ";
        fs<<std::to_string(joint_desired_pose[9]);
        fs<<", ";
        fs<<std::to_string(0);
        fs<<", ";
        fs<<'\n';
        fs.close();
}

int main(int argc, char **argv)
{
    bool iiwa1 = false;
    bool iiwa2 = true;
    bool read_write = true;

    ros::init(argc, argv, "tele_iiwa");
    ros::NodeHandle nh;
    // ros spinner
    ros::AsyncSpinner spinner(0);
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


    // *** decleare ***
    // services
    iiwa_ros::service::ControlModeService control_mode2;
    iiwa_ros::service::PathParametersService j_vel2;

    iiwa_ros::service::PathParametersLinService c_vel2;
    iiwa_ros::service::TimeToDestinationService time_to_dist2;
    // commands
    iiwa_ros::command::CartesianPose cp_command2;
    iiwa_ros::command::CartesianPoseLinear cpl_command2;
    iiwa_ros::command::JointPosition jp_command2;
    iiwa_ros::command::JointVelocity jv_command2;
    // states
    iiwa_ros::state::CartesianWrench cw_state2;
    iiwa_ros::state::CartesianPose cp_state2;
    iiwa_ros::state::JointVelocity jv_state2;
    iiwa_ros::state::JointPosition jp_state2;
    iiwa_ros::state::ExternalJointTorque exjt_state2;
    // cartesian position msg
    geometry_msgs::PoseStamped init_pos2, new_pose2;
    // cartesian velocity msg
    geometry_msgs::Twist cartesian_velocity2;


    double vel = 0.75;
    double Jvel = 0.15;
    // cartesian_velocity.linear.x = vel;
    // cartesian_velocity.linear.y = vel;
    // cartesian_velocity.linear.z = vel;
    // cartesian_velocity.angular.x = vel;
    // cartesian_velocity.angular.y = vel;
    // cartesian_velocity.angular.z = vel;
    ros::Subscriber sub = nh.subscribe("/exoskeleton_data", 1, pose_callback);

    ros::spinOnce();
    // *** initialize ***
    if (iiwa1 == true){
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
        j_vel.setSmartServoJointSpeedLimits(0.30, 0.30);

    }

    if (iiwa2 == true){
        control_mode2.init("iiwa2");
        j_vel2.init("iiwa2");
        c_vel2.init("iiwa2");
        time_to_dist2.init("iiwa2");
        // commands
        cp_command2.init("iiwa2");
        cpl_command2.init("iiwa2");
        jp_command2.init("iiwa2");
        jv_command2.init("iiwa2");
        // states
        cw_state2.init("iiwa2");
        cp_state2.init("iiwa2");
        jv_state2.init("iiwa2");
        jp_state2.init("iiwa2");
        exjt_state2.init("iiwa2");
        j_vel2.setSmartServoJointSpeedLimits(0.5, 0.5);
    }


    ros::Duration(0.1).sleep(); // wait to initialize ros topics

    int skipper = -1000000;
    time_t curr_time;
    curr_time = time(NULL);
    nanoseconds ns_init = duration_cast< nanoseconds >(system_clock::now().time_since_epoch());
    using namespace std;

    ros::Publisher force_IIWA2 = nh.advertise<std_msgs::Float32MultiArray>("Force_iiwa2", 10);
    ros::Publisher force_IIWA = nh.advertise<std_msgs::Float32MultiArray>("Force_iiwa", 10);

    ros::Publisher pos_IIWA2 = nh.advertise<std_msgs::Float32MultiArray>("pos_iiwa2", 10);
    ros::Publisher pos_IIWA = nh.advertise<std_msgs::Float32MultiArray>("pos_iiwa", 10);

    int skiper = 0;
    while (true)
    {
        if (iiwa1 == true){
            auto cartesian_position = cp_state.getPose();
            auto joint_position = jp_state.getPosition();
            auto force = exjt_state.getTorque();
            auto joint_speed = jv_state.getVelocity();

            joint_position.position.a1 = joint_desired_pose[0];
            joint_position.position.a2 = (joint_desired_pose[1] + 3.14/4 + 0.15)*0.8;
            if(joint_position.position.a2 > 1.15){
                joint_position.position.a2 = 1.15;
            }
            joint_position.position.a4 = (-joint_desired_pose[2] - 3.14/2 - 3.14/4)*0.8;
            cout<<joint_position.position.a4<<endl;
            if(joint_position.position.a4 < -1.8){
                joint_position.position.a4 = -1.8;
            }
            joint_position.position.a5 = joint_desired_pose[3];
            // std::cout<<std::to_string(cartesian_position.poseStamped.pose.position.z)<<std::endl;
            // joint_position.position.a6 = 0;

            joint_position.position.a6 = joint_desired_pose[4];
            if (joint_position.position.a6 > 0.0){
                joint_position.position.a6 = 0;
            }
            jp_command.setPosition(joint_position);

            if (read_write == true){
                time_t curr_time;
                curr_time = time(NULL);
                nanoseconds ns = duration_cast< nanoseconds >(system_clock::now().time_since_epoch());
                time_t mnow = curr_time;
                std::fstream fs;
                fs.open ("datas_iiwa1_coord.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(joint_position.position.a1);
                fs<<", ";
                fs<<std::to_string(joint_position.position.a2);
                fs<<", ";
                fs<<std::to_string(joint_position.position.a3);
                fs<<", ";
                fs<<std::to_string(joint_position.position.a4);
                fs<<", ";
                fs<<std::to_string(joint_position.position.a5);
                fs<<", ";
                fs<<std::to_string(joint_position.position.a6);
                fs<<", ";
                fs<<std::to_string(joint_position.position.a7);
                fs<<", ";
                fs<<'\n';
                fs.close();

                fs.open ("datas_iiwa1_speed.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a1);
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a2);
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a3);
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a4);
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a5);
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a6);
                fs<<", ";
                fs<<std::to_string(joint_speed.velocity.a7);
                fs<<", ";
                fs<<'\n';
                fs.close();

                fs.open ("datas_iiwa_force.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(force.torque.a1);
                fs<<", ";
                fs<<std::to_string(force.torque.a2);
                fs<<", ";
                fs<<std::to_string(force.torque.a3);
                fs<<", ";
                fs<<std::to_string(force.torque.a4);
                fs<<", ";
                fs<<std::to_string(force.torque.a5);
                fs<<", ";
                fs<<std::to_string(force.torque.a6);
                fs<<", ";
                fs<<std::to_string(force.torque.a7);
                fs<<", ";
                fs<<'\n';
                fs.close();

                fs.open ("datas_iiwa1_cartesian_pos.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(cartesian_position.poseStamped.pose.position.x);
                fs<<", ";
                fs<<std::to_string(cartesian_position.poseStamped.pose.position.y);
                fs<<", ";
                fs<<std::to_string(cartesian_position.poseStamped.pose.position.z);
                fs<<", ";
                fs<<'\n';
                fs.close();
            }
        }

        if(iiwa2 == true){
            auto cartesian_position2 = cp_state2.getPose();
            auto joint_position2 = jp_state2.getPosition();
            auto force2 = exjt_state2.getTorque();
            auto joint_speed2 = jv_state2.getVelocity();

            if (read_write == true and skiper%10 == 0){
                time_t curr_time;
                curr_time = time(NULL);
                nanoseconds ns = duration_cast< nanoseconds >(system_clock::now().time_since_epoch());
                time_t mnow = curr_time;
                std::fstream fs;
                fs.open ("datas_iiwa2.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a1);
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a2);
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a3);
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a4);
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a5);
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a6);
                fs<<", ";
                fs<<std::to_string(joint_position2.position.a7);
                fs<<", ";
                fs<<'\n';
                fs.close();

                fs.open ("datas_iiwa2_speed.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a1);
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a2);
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a3);
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a4);
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a5);
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a6);
                fs<<", ";
                fs<<std::to_string(joint_speed2.velocity.a7);
                fs<<", ";
                fs<<'\n';
                fs.close();

                fs.open ("datas_iiwa2_force.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(force2.torque.a1);
                fs<<", ";
                fs<<std::to_string(force2.torque.a2);
                fs<<", ";
                fs<<std::to_string(force2.torque.a3);
                fs<<", ";
                fs<<std::to_string(force2.torque.a4);
                fs<<", ";
                fs<<std::to_string(force2.torque.a5);
                fs<<", ";
                fs<<std::to_string(force2.torque.a6);
                fs<<", ";
                fs<<std::to_string(force2.torque.a7);
                fs<<", ";
                fs<<'\n';
                fs.close();

                fs.open ("datas_iiwa2_cartesian_pos.txt", std::fstream::in | std::fstream::out | std::fstream::app);
                fs<<"Time  ";
                fs<< std::to_string((ns).count());
                fs<<", ";
                fs<<std::to_string(cartesian_position2.poseStamped.pose.position.x);
                fs<<", ";
                fs<<std::to_string(cartesian_position2.poseStamped.pose.position.y);
                fs<<", ";
                fs<<std::to_string(cartesian_position2.poseStamped.pose.position.z);
                fs<<", ";
                fs<<'\n';
                fs.close();
            }

            joint_position2.position.a1 = joint_desired_pose[5]*0.7;
            joint_position2.position.a2 = (-joint_desired_pose[6] + 3.14/4 +0.1)*0.8;
            if(joint_position2.position.a2 > 1){
                joint_position2.position.a2 = 1;
            }
            joint_position2.position.a4 = (joint_desired_pose[7] - 3.14/2 - 3.14/4)*0.8;
            if(joint_position2.position.a4 < -1.7){
                joint_position2.position.a4 = -1.7;
            }

            joint_position2.position.a5 = (joint_desired_pose[8])*0.8;
            // std::cout << to_string(joint_position2.position.a5) << std::endl;

            joint_position2.position.a6 = -joint_desired_pose[9]*0.8;
            joint_position2.position.a7 = 3.14/2;
            jp_command2.setPosition(joint_position2);
            skiper++;

        }
    }
}
