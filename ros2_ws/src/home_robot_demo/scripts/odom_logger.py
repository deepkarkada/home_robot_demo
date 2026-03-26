import csv
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomLogger(Node):
    def __init__(self):
        super().__init__('odom_logger')

        self.sub = self.create_subscription(
            Odometry,
            '/diff_drive_controller/odom',
            self.cb,
            10
        )

        self.file = open('/tmp/odom_log.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            't', 'x', 'y', 'z',
            'qx', 'qy', 'qz', 'qw',
            'vx', 'vy', 'vz',
            'wx', 'wy', 'wz'
        ])

    def cb(self, msg):
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        lv = msg.twist.twist.linear
        av = msg.twist.twist.angular

        self.writer.writerow([
            t,
            p.x, p.y, p.z,
            q.x, q.y, q.z, q.w,
            lv.x, lv.y, lv.z,
            av.x, av.y, av.z
        ])
        self.file.flush()

def main():
    rclpy.init()
    node = OdomLogger()
    try:
        rclpy.spin(node)
    finally:
        node.file.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()