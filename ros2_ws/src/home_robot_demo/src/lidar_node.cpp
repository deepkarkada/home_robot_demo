#include <memory>
#include <algorithm>
#include <cmath>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "geometry_msgs/msg/twist_stamped.hpp"

class LidarAvoidanceNode : public rclcpp::Node
{
public:
  LidarAvoidanceNode()
  : Node("lidar_avoidance_node")
  {
    cmd_pub_ = this->create_publisher<geometry_msgs::msg::TwistStamped>(
      "/diff_drive_controller/cmd_vel", 10);

    scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
      "/scan", 10,
      std::bind(&LidarAvoidanceNode::scanCallback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "Lidar avoidance node started");
  }

private:
  void scanCallback(const sensor_msgs::msg::LaserScan::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(),
      "Received scan with %zu ranges", msg->ranges.size());

    geometry_msgs::msg::TwistStamped cmd;
    cmd.header.stamp = this->now();
    cmd.header.frame_id = "chassis";

    bool all_more = true;

    for (const auto & range : msg->ranges)
    {
      if (std::isfinite(range) && range < 1.0)
      {
        all_more = false;
        break;
      }
    }

    if (all_more)
    {
      cmd.twist.linear.x = 0.5;
      cmd.twist.angular.z = 0.0;
    }
    else
    {
      cmd.twist.linear.x = 0.0;
      cmd.twist.angular.z = 0.5;
    }

    RCLCPP_INFO(this->get_logger(),
      "Publishing cmd linear=%.2f angular=%.2f",
      cmd.twist.linear.x, cmd.twist.angular.z);

    cmd_pub_->publish(cmd);
  }

  rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr cmd_pub_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<LidarAvoidanceNode>());
  rclcpp::shutdown();
  return 0;
}