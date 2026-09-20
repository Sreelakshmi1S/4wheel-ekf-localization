#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    description_share = get_package_share_directory(
        "four_wheel_robot_description")
    ros_gz_sim_share = get_package_share_directory("ros_gz_sim")

    xacro_path = os.path.join(
        description_share,
        "urdf",
        "robots",
        "4wd.urdf.xacro",)

    # Start Gazebo Fortress with its standard empty world.
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_sim_share,
                "launch",
                "gz_sim.launch.py",)),launch_arguments={"gz_args": "-r empty.sdf",}.items(),)

    # Convert the Xacro model into a URDF string.
    robot_description = ParameterValue(Command(["xacro ", xacro_path]),value_type=str,)

    # Publish the robot's link transforms.
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }],)

    # Spawn the URDF published on /robot_description into Gazebo.
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_four_wheel_robot",
        output="screen",
        arguments=[
            "-topic",
            "/robot_description",
            "-name",
            "four_wheel_robot",
            "-z",
            "0.05",
        ],
    )

    # Bridge simulation time, velocity commands, joint states, and
    # Gazebo drivetrain odometry.
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="simulation_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist",
            "/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model",
            "/gazebo/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry",
        ],
    )

    return LaunchDescription([
            gz_sim,
            robot_state_publisher,
            spawn_robot,
            bridge,])

