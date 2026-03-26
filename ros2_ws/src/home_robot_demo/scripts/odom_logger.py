import csv
import math
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

        self.start_x = None
        self.start_y = None
        self.prev_x = None
        self.prev_y = None
        self.path_length = 0.0
        self.last_print_time = 0.0

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

        x = p.x
        y = p.y

        if self.start_x is None:
            self.start_x = x
            self.start_y = y
            self.prev_x = x
            self.prev_y = y

        step_dist = math.hypot(x - self.prev_x, y - self.prev_y)
        self.path_length += step_dist

        displacement = math.hypot(x - self.start_x, y - self.start_y)

        self.writer.writerow([
            t,
            p.x, p.y, p.z,
            q.x, q.y, q.z, q.w,
            lv.x, lv.y, lv.z,
            av.x, av.y, av.z,
            displacement,
            self.path_length
        ])
        self.file.flush()

        # print at ~2 Hz instead of every callback
        if t - self.last_print_time >= 0.5:
            self.get_logger().info(
                f"x={x:.3f}, y={y:.3f}, "
                f"displacement={displacement:.3f} m, "
                f"path_length={self.path_length:.3f} m"
            )
            self.last_print_time = t

        self.prev_x = x
        self.prev_y = y

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