#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

scene = moveit_commander.PlanningSceneInterface()

arm_name = "arm_group"
hand_name = "hand_group"
arm_group = moveit_commander.MoveGroupCommander(arm_name)
arm_group.set_planner_id("RRTConnectkConfigDefault")
arm_group.set_planning_time(10)

current_robot2_pose = arm_group.get_current_pose()
print current_robot2_pose

# put the arm at the 1st grasping position
pose_target = geometry_msgs.msg.Pose()
pose_target.position.x = current_robot2_pose.pose.position.x 
pose_target.position.y = current_robot2_pose.pose.position.y 
pose_target.position.z = current_robot2_pose.pose.position.z + 0.5

arm_group.set_pose_target(pose_target)

#plan1 = arm_group.plan()
plan1 = arm_group.go()
print plan1

rospy.sleep(3)
moveit_commander.roscpp_shutdown()