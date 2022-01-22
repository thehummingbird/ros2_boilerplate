from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
  return LaunchDescription([
      Node(
          package='brain',
          namespace='common',
          executable='brain',
          name='tester'
      ),
      Node(
          package='perception',
          namespace='common',
          executable='perception',
          name='tester'
      )
  ])
