import rclpy
import json
from rclpy.node import Node

from std_msgs.msg import String

import jsonHandler
import jsonObject


class MapLoaderNode(Node):

    def __init__(self):
        super().__init__('MapLoaderNode')
        self.publisher_ = self.create_publisher(String, 'map_to_sim', 10)
        self.subscription = self.create_subscription(
            String,
            'sim_to_map',
            self.listener_callback,
            10)
        self.subscription

    def timer_callback(self):
        msg = String()
        object = jsonHandler.getJsonObject("zadanie1.json")
        msg.data = json.dumps(jsonHandler.createJsonObject(object.x, object.y, object.sizeOfTile, object.actor["x"], object.actor["y"],object.map))
        self.publisher_.publish(msg)

    def listener_callback(self, msg):
        dict = json.loads(msg.data)
        object = jsonObject.Json(**dict)
        
        data = jsonHandler.createJsonObject(object.x, object.y, object.sizeOfTile, object.actor["x"], object.actor["y"],object.map)
        jsonHandler.changeJson("zadanie1.json",data)
        self.timer_callback()

def main(args=None):
    rclpy.init(args=args)

    node = MapLoaderNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()