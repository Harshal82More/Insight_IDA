#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import actionlib
import geometry_msgs

def simple_pick_place():
  ## First initialize moveit_commander and rospy.
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('simple_pick_place',
                  anonymous=True)

  ## Instantiate a MoveGroupCommander object.  This object is an interface
  ## to one group of joints.  In this case the group refers to the joints of
  ## robot1. This interface can be used to plan and execute motions on robot1.
  arm_group = moveit_commander.MoveGroupCommander("arm_group")
  ## MoveGroup Commander Object for robot2.
  hand_group = moveit_commander.MoveGroupCommander("hand_group")

  arm_group.set_planner_id("RRTConnectkConfigDefault")
  arm_group.set_planning_time(10)
  
  ## Action clients to the ExecuteTrajectory action server.
  arm_client = actionlib.SimpleActionClient('execute_trajectory', 
      moveit_msgs.msg.ExecuteTrajectoryAction)
  arm_client.wait_for_server()
  rospy.loginfo('Execute Trajectory server is available for arm')

  hand_client = actionlib.SimpleActionClient('execute_trajectory', 
      moveit_msgs.msg.ExecuteTrajectoryAction)
  hand_client.wait_for_server()
  rospy.loginfo('Execute Trajectory server is available for hand')
  
  hand_group.set_named_target("open")                            ## Named joint configurations are the robot poses defined via MoveIt! Setup Assistant.
  plan = hand_group.plan()                                       ## Plan to the desired joint-space goal using the default planner (RRTConnect).
  hand_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()            ## Create a goal message object for the action server.
  hand_goal.trajectory = plan                                    ## Update the trajectory in the goal message.
  hand_client.send_goal(hand_goal)                               ## Send the goal to the action server.
  hand_client.wait_for_result()
  arm_group.stop()
  arm_group.clear_pose_targets()
  
  ## Set a named joint configuration as the goal to plan for a move group.
  arm_group.set_named_target("pick_2")
  plan = arm_group.plan()
  arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
  arm_goal.trajectory = plan
  arm_client.send_goal(arm_goal)
  arm_client.wait_for_result()
  arm_group.stop()
  arm_group.clear_pose_targets()

  hand_group.set_named_target("close")                            ## Named joint configurations are the robot poses defined via MoveIt! Setup Assistant.
  plan = hand_group.plan()                                       ## Plan to the desired joint-space goal using the default planner (RRTConnect).
  hand_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()            ## Create a goal message object for the action server.
  hand_goal.trajectory = plan                                    ## Update the trajectory in the goal message.
  hand_client.send_goal(hand_goal)                               ## Send the goal to the action server.
  hand_client.wait_for_result()
  arm_group.stop()
  arm_group.clear_pose_targets()


  #  ## Cartesian Paths
  # ## ^^^^^^^^^^^^^^^
  # ## You can plan a cartesian path directly by specifying a list of waypoints
  # ## for the end-effector to go through.
  waypoints = []
  # start with the current pose
  current_pose = arm_group.get_current_pose()
  rospy.sleep(10)
  current_pose = arm_group.get_current_pose()

  print current_pose

  ## create linear offsets to the current pose
  new_eef_pose = geometry_msgs.msg.Pose()

  # Manual offsets because we don't have a camera to detect objects yet.
  new_eef_pose.position.x = current_pose.pose.position.x + 0.10
  new_eef_pose.position.y = current_pose.pose.position.y - 0.20
  new_eef_pose.position.z = current_pose.pose.position.z - 0.20
  
  new_eef_pose.orientation = copy.deepcopy(current_pose.pose.orientation)
  waypoints.append(new_eef_pose)
  waypoints.append(current_pose.pose)

  ## We want the cartesian path to be interpolated at a resolution of 1 cm
  ## which is why we will specify 0.01 as the eef_step in cartesian
  ## translation.  We will specify the jump threshold as 0.0, effectively
  ## disabling it.
  fraction = 0.0
  for count_cartesian_path in range(0,3):
    if fraction < 1.0:
      (plan_cartesian, fraction) = arm_group.compute_cartesian_path(
                                   waypoints,   # waypoints to follow
                                   0.01,        # eef_step
                                   0.0)         # jump_threshold
    else:
      break

  arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
  arm_goal.trajectory = plan_cartesian

  arm_client.send_goal(arm_goal)
  arm_client.wait_for_result()
  
  current_pose = arm_group.get_current_pose()
  rospy.sleep(10)
  current_pose = arm_group.get_current_pose()
  print current_pose
  
  arm_group.set_named_target("drop_3")
  plan = arm_group.plan()
  arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
  arm_goal.trajectory = plan
  arm_client.send_goal(arm_goal)
  arm_client.wait_for_result()
  arm_group.stop()
  arm_group.clear_pose_targets()

  print current_pose
  ## When finished shut down moveit_commander.
  moveit_commander.roscpp_shutdown()


if __name__=='__main__':
  try:
    simple_pick_place()
  except rospy.ROSInterruptException:
    pass