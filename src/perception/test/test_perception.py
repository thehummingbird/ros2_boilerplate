import os
import sys
import time
import unittest
import uuid

from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription


import launch
import launch_ros
import launch_ros.actions
import launch_testing.actions
import launch_testing_ros

import pytest

import rclpy

import std_msgs.msg


@pytest.mark.rostest
def generate_test_description():
  # Normally, talker publishes on the 'chatter' topic and listener listens on the
  # 'chatter' topic, but we want to show how to use remappings to munge the data so we
  # will remap these topics when we launch the nodes and insert our own node that can
  # change the data as it passes through
  path_to_test = os.path.dirname(__file__)
  package_prefix = get_package_share_directory('perception')
  perception_node = launch_ros.actions.Node(
      executable=sys.executable,
      arguments=[os.path.join(
          path_to_test, '../perception/perception_node.py')],
      additional_env={'PYTHONUNBUFFERED': '1'},
      remappings=[('topic', 'topic2')]
  )

  # return launch.LaunchDescription([
  #     IncludeLaunchDescription(
  #         PythonLaunchDescriptionSource(
  #             [package_prefix, '/launch/perception.launch.py'])
  #     ),
  #     launch_testing.actions.ReadyToTest()
  # ])
  return (
      launch.LaunchDescription([
          perception_node,
          # Start tests right away - no need to wait for anything
          launch_testing.actions.ReadyToTest(),
      ]),
      {
          'perception': perception_node,
      }
  )


class TestTalkerListenerLink(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    # Initialize the ROS context for the test node
    rclpy.init()

  @classmethod
  def tearDownClass(cls):
    # Shutdown the ROS context
    rclpy.shutdown()

  def setUp(self):
    # Create a ROS node for tests
    self.node = rclpy.create_node('test_talker_listener_link')

  def tearDown(self):
    self.node.destroy_node()

  def test_perception_transmits(self, launch_service, perception, proc_output):
    # Expect the talker to publish strings on '/talker_chatter' and also write to stdout
    msgs_rx = []

    sub = self.node.create_subscription(
        std_msgs.msg.String,
        'topic2',
        lambda msg: msgs_rx.append(msg),
        10
    )
    try:
      # Wait until the talker transmits two messages over the ROS topic
      end_time = time.time() + 20
      while time.time() < end_time:
        rclpy.spin_once(self.node, timeout_sec=0.1)
        if len(msgs_rx) > 2:
          break

      self.assertGreater(len(msgs_rx), 2)

      # Make sure the talker also output the same data via stdout
      for msg in msgs_rx:
        proc_output.assertWaitFor(
            expected_output=msg.data, process=perception
        )
    finally:
      self.node.destroy_subscription(sub)
