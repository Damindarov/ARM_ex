#include <iiwa_ros.h>
#include <cmath>
#include <std_msgs/Bool.h>
#include <unistd.h>
// getTimeToDestination() can also return negative values and the info from the cabinet take some milliseconds to update once the motion is started.
// That means that if you call getTimeToDestination() right after you set a target pose, you might get the wrong info (e.g. a negative number).
// This function tried to call getTimeToDestination() until something meaningful is obtained or until a maximum amount of time passed.
void sleepForMotion(iiwa_ros::iiwaRos& iiwa, const double maxSleepTime) {
  double ttd = iiwa.getTimeToDestinationService().getTimeToDestination();
  ros::Time start_wait = ros::Time::now();
  while (ttd < 0.0 && (ros::Time::now() - start_wait) < ros::Duration(maxSleepTime)) {
    ros::Duration(0.5).sleep();
    ttd = iiwa.getTimeToDestinationService().getTimeToDestination();
  }
  if (ttd > 0.0) {
    ROS_INFO_STREAM("Sleeping for " << ttd << " seconds.");
    ros::Duration(ttd).sleep();
  } 
}
bool comp(int a, int b) 
{ 
    return (a < b); 
} 

bool atPosition(geometry_msgs::PoseStamped current, geometry_msgs::PoseStamped command)
{
	double e[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
	double max_e; 
	e[0] = fabs(current.pose.position.x-command.pose.position.x);
	e[1] = fabs(current.pose.position.y-command.pose.position.y);
	e[2] = fabs(current.pose.position.z-command.pose.position.z);
	e[3] = fabs(current.pose.orientation.x-command.pose.orientation.x);
	e[4] = fabs(current.pose.orientation.y-command.pose.orientation.y);
	e[5] = fabs(current.pose.orientation.z-command.pose.orientation.z);
	e[6] = fabs(current.pose.orientation.w-command.pose.orientation.w);
	max_e = *std::max_element(e,e+7);
	ROS_INFO("error: %f ", max_e);
	if (max_e<0.01)
	{return true;}
	else 
	return false;
}

int main (int argc, char **argv) {
	
	// Initialize ROS
	ros::init(argc, argv, "CommandRobot");
	ros::NodeHandle nh("~");
	// initialize the publisher
	ros::Publisher gripperCommand = nh.advertise<std_msgs::Bool>("/iiwa/command/GripperCommand", 1000);

	// ROS spinner.
	ros::AsyncSpinner spinner(1);
	spinner.start();

	iiwa_ros::iiwaRos my_iiwa;
	my_iiwa.init();
			
	ros::Rate rate(1);
  
  	geometry_msgs::PoseStamped command_cartesian_position;
	geometry_msgs::PoseStamped current_cartesian_position;

	bool new_pose = false, motion_done = false;
	std_msgs::Bool grasp;
	grasp.data = false;
	int pos = 0;
	std::vector<std::vector<float>> cartesian_pose;
	cartesian_pose = {{0.400, -0.0, 0.650, 0.5626401, 0.0, -0.5626401, -0.6056999},
					{0.010, -0.500, 0.470, 0.5626401, 0.0, -0.5626401, -0.6056999},
					{0.010, -0.540, 0.320, 0.5626401, 0.0, -0.5626401, -0.6056999},
					{0.010, -0.500, 0.470, 0.5626401, 0.0, -0.5626401, -0.6056999},
					{-0.226, -0.447, 0.470, 0.5626401, 0.0, -0.5626401, -0.6056999},
					{-0.245, -0.484, 0.322, 0.5626401, 0.0, -0.5626401, -0.6056999},
					{-0.226, -0.447, 0.470, 500.5626401, 0.0, -0.5626401, -0.6056999},
					{0.422, -0.030, 0.650, 0.0, 0.0, -0.0, 1.0}};
	
	while (ros::ok()) {
    if (my_iiwa.getRobotIsConnected()) 
	{		
		if (pos == 8)
		{
			ros::shutdown();
			break;
		}
		else
		{
			command_cartesian_position.pose.position.x = cartesian_pose[pos][0];
			command_cartesian_position.pose.position.y = cartesian_pose[pos][1];
			command_cartesian_position.pose.position.z = cartesian_pose[pos][2];
			command_cartesian_position.pose.orientation.x = cartesian_pose[pos][3];
			command_cartesian_position.pose.orientation.y = cartesian_pose[pos][4];
			command_cartesian_position.pose.orientation.z = cartesian_pose[pos][5];
			command_cartesian_position.pose.orientation.w = cartesian_pose[pos][6];
			if (pos == 3)
			{
				grasp.data = true;
				gripperCommand.publish(grasp);
				usleep(1000000);
			}
			if (pos == 6)
			{
				grasp.data = false;
				gripperCommand.publish(grasp);
				usleep(1000000);
			}
			usleep(1000000);
			//rate.sleep();
			my_iiwa.setCartesianPose(command_cartesian_position);
			while (!my_iiwa.getCartesianPose(current_cartesian_position)) {
				//ROS_INFO("getJointPosition");
				}
			while (!atPosition(current_cartesian_position, command_cartesian_position))
			{
				while (!my_iiwa.getCartesianPose(current_cartesian_position)){}
				//ROS_INFO("atPosition");
			}			
			sleepForMotion(my_iiwa, 2.0);
			pos += 1;
		}
	}
	else {
		ROS_WARN_STREAM("Robot is not connected...");
		ros::Duration(5.0).sleep(); // 5 seconds
	}
	}	
}; 
