#! /usr/bin/env python
import sys
import rospy
import moveit_commander
import tf
import tf2_ros
import tf2_geometry_msgs
import geometry_msgs

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()

# Put the arm in the start position
arm_group = moveit_commander.MoveGroupCommander("arm_group")
hand_group = moveit_commander.MoveGroupCommander("hand_group")
arm_group.set_named_target("pick_2")
plan1 = arm_group.go()


# Declate a TF buffer globally.
# get the pose
t = tf.TransformListener ()


if t.frameExists("/base_link") and t.frameExists("/grapple"):
    (translation,rotation) = t.lookupTransform("base_link", "grapple", rospy.Time())
    print translation
    print rotation

    # put the arm at the 1st grasping position
    pose_target = geometry_msgs.msg.Pose()
    pose_target.orientation.w = 0.5
    pose_target.orientation.x = -0.5
    pose_target.orientation.y = 0.5
    pose_target.orientation.z = -0.5
    pose_target.position = translation
    pose_target.position.z -= 0.15
    arm_group.set_pose_target(pose_target)
    plan1 = arm_group.go()

    # put the arm at the 2nd grasping position
    pose_target.position.z += 0.15
    arm_group.set_pose_target(pose_target)
    plan1 = arm_group.go()
    
    # Open the gripper
    hand_group.set_named_target("close")
    plan2 = hand_group.go()
    
    # Put the arm in the start position
    arm_group.set_named_target("")
    plan1 = arm_group.go()
  

rospy.sleep(5)
moveit_commander.roscpp_shutdown()