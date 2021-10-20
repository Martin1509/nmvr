import rclpy
import map
from rclpy.node import Node

from std_msgs.msg import String


class Simulator(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'sim_to_map', 10)
        self.subscription = self.create_subscription(
            String,
            'map_to_sim',
            self.listener_callback,
            10)
        self.subscription
        timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        map.init()
    
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    simulator = Simulator()

    rclpy.spin(simulator)

    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

