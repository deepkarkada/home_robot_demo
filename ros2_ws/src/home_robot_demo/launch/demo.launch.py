import os
from launch import LaunchDescription
from launch.actions import OpaqueFunction, SetEnvironmentVariable, ExecuteProcess
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def launch_setup(context, *args, **kwargs):
    pkg_share = FindPackageShare("home_robot_demo").perform(context)

    model_template = os.path.join(
        pkg_share, "models", "vehicle", "model.sdf.in"
    )
    controllers_yaml = os.path.join(
        pkg_share, "config", "controllers.yaml"
    )
    world_path = os.path.join(
        pkg_share, "worlds", "home_world_two_rooms.sdf"
    )

    # You need to create this URDF file
    urdf_path = os.path.join(pkg_share, "urdf", "vehicle.urdf")

    generated_models_root = os.path.join(
        pkg_share, "models_generated"
    )
    generated_model_dir = os.path.join(
        generated_models_root, "vehicle"
    )
    os.makedirs(generated_model_dir, exist_ok=True)

    generated_model_sdf = os.path.join(generated_model_dir, "model.sdf")
    generated_model_config = os.path.join(
        pkg_share, "models", "vehicle", "model.config"
    )
    generated_model_config_out = os.path.join(generated_model_dir, "model.config")

    with open(model_template, "r") as f:
        sdf_text = f.read()

    sdf_text = sdf_text.replace("{{CONTROLLERS_YAML}}", controllers_yaml)

    with open(generated_model_sdf, "w") as f:
        f.write(sdf_text)

    # copy model.config into generated folder if needed
    if os.path.exists(generated_model_config):
        with open(generated_model_config, "r") as src, open(generated_model_config_out, "w") as dst:
            dst.write(src.read())

    gz_resource_paths = [
        generated_models_root,
        os.path.join(pkg_share, "models"),
    ]

    existing = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    if existing:
        gz_resource_value = ":".join(gz_resource_paths + [existing])
    else:
        gz_resource_value = ":".join(gz_resource_paths)

    existing_plugin_path = os.environ.get("GZ_SIM_SYSTEM_PLUGIN_PATH", "")
    plugin_path = "/opt/ros/jazzy/lib"
    if existing_plugin_path:
        plugin_path = plugin_path + ":" + existing_plugin_path

    with open(urdf_path, "r") as f:
        robot_description = f.read()

    odom_logger_path = os.path.join(pkg_share, "scripts", "odom_logger.py")

    return [
        SetEnvironmentVariable(
            name="GZ_SIM_RESOURCE_PATH",
            value=gz_resource_value,
        ),
        SetEnvironmentVariable(
            name="GZ_SIM_SYSTEM_PLUGIN_PATH",
            value=plugin_path,
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description}],
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
            output="screen",
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=["/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan"],
            output="screen",
        ),

        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_broadcaster", "-c", "/controller_manager"],
            output="screen",
        ),

        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["diff_drive_controller", "-c", "/controller_manager"],
            output="screen",
        ),
        Node(
            package="home_robot_demo",
            executable="lidar_node",
            output="screen",
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/camera/image@sensor_msgs/msg/Image@gz.msgs.Image"
            ],
            output="screen",
        ),
        ExecuteProcess(
            cmd=["gz", "sim", "-r", world_path],
            output="screen",
        ),
        ExecuteProcess(
            cmd=["python3", "-u", odom_logger_path],
            output='screen'
        ),

    ]


def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])