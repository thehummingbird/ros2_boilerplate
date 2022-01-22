from launch_ros.actions import Node


def generate_launch_description():
  return LaunchDescription([
      Node(
          package='perception',
          namespace='common',
          executable='perception',
          name='tester'
      )
  ])
