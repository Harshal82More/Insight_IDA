#! /usr/bin/env python
### Forword Kinematics ###
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

# Moveit commander interphase for mython and Moviet
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()    
group = moveit_commander.MoveGroupCommander("arm_group")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

# Joint starting from link_1 to gripper
group_variable_values = group.get_current_joint_values()
group_variable_values[0] = 0.5
group_variable_values[1] = 0.2
group_variable_values[2] = 0.3
group_variable_values[3] = 0.3

# Whaterver input is above for each joint is target now.
group.set_joint_value_target(group_variable_values)

plan2 = group.plan()
group.go(wait=True)

rospy.sleep(3)

moveit_commander.roscpp_shutdown()

print "Reference frame: %s" % group.get_planning_frame()
print "End effector: %s" % group.get_end_effector_link()
print "Robot Groups:"
print robot.get_group_names()
print "Current Joint Values:"
print group.get_current_joint_values()
print "Current Pose:"
print group.get_current_pose()
print "Robot State:"
print robot.get_current_state()
