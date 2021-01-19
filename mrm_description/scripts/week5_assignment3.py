#!/usr/bin/env python
import rospy
from mrm_description.msg import camera2
import tf2_ros
import tf2_geometry_msgs
import geometry_msgs

# Declare a TF buffer globally.
tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)

def logical_camera2_callback(data):
  # Check if the logical camera has seen our box which has the name 'object'.
  if (data.models[-1].type == 'object'):
    # Create a pose stamped message type from the camera image topic.
    object_pose = geometry_msgs.msg.PoseStamped()
    object_pose.header.stamp = rospy.Time.now()
    object_pose.header.frame_id = "camera_2"
    object_pose.pose.position.x = data.models[-1].pose.position.x
    object_pose.pose.position.y = data.models[-1].pose.position.y
    object_pose.pose.position.z = data.models[-1].pose.position.z
    object_pose.pose.orientation.x = data.models[-1].pose.orientation.x
    object_pose.pose.orientation.y = data.models[-1].pose.orientation.y
    object_pose.pose.orientation.z = data.models[-1].pose.orientation.z
    object_pose.pose.orientation.w = data.models[-1].pose.orientation.w
    while True:
      try:
        object_world_pose = tf_buffer.transform(object_pose, "vacuum_gripper2_suction_cup")
        break
      except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        continue
    rospy.loginfo('Pose of the object in the vacuum_gripper2_suction_cup reference frame is: %s', object_world_pose)
    rospy.loginfo('Pose of the object in the reference framecamera of logical camera2 is: %s', object_pose)
    # Gracefully terminate the ROS node after transforming the pose.
    rospy.signal_shutdown('Successfully transformed pose.')
  else:
    # Do nothing.
    print('')

if __name__== '__main__':
  # Initialize ROS node to transform object pose.
  rospy.init_node('week5_assignment3',
                    anonymous=True)

  # Subscribe to the logical camera topic.
  rospy.Subscriber('mrm/camera1', camera2, logical_camera2_callback)

  rospy.spin()
