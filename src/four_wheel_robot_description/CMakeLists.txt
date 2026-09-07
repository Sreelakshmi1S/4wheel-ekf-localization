cmake_minimum_required(VERSION 3.8)
project(four_wheel_robot_description)

find_package(ament_cmake REQUIRED)

# Install robot-description resources into the ROS package share directory.
install(
  DIRECTORY
    launch
    meshes
    rviz
    urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
