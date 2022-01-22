import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from custom_interfaces.srv import ComponentStatus


class PerceptionNode(Node):

  def __init__(self):
    super().__init__('perception_node')

    self._publisher = self.create_publisher(
        String,
        'topic',
        10
    )
    timerPeriod = 1  # seconds
    self.timer = self.create_timer(timerPeriod, self.timer_callback)
    self.count = 0

    self.componentStatusService = self.create_service(
        ComponentStatus,
        'component_status',
        self.handle_component_status
    )

  def timer_callback(self):
    msg = String()
    if (self.count % 10 == 0):
      msg.data = "I see trash"
    else:
      msg.data = "I see nothing"
    self._publisher.publish(msg)
    self.get_logger().info('Publishing: "%s"' % msg.data)
    self.count += 1

  def handle_component_status(self, request, response):
    self.get_logger().info("Server called!")
    if request.component == "camera":
      response.status = "Camera Battery is at 100%"

      return response


def main(args=None):
  rclpy.init(args=args)

  perceptionNode = PerceptionNode()

  rclpy.spin(perceptionNode)

  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  perceptionNode.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()
