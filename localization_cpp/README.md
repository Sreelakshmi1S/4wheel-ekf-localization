# localization_cpp

Custom C++ ROS2 nodes for this project. This is the primary hand-written code
in the repository — the sensor fusion math itself is handled by the
battle-tested `robot_localization` package, but the integration layer is custom.

**Planned nodes:**
- `marker_pose_bridge_node` — subscribes to ArUco marker detections
  (`ros2_aruco` / `aruco_opencv` message types), converts them into
  `geometry_msgs/PoseWithCovarianceStamped` on the topic `robot_localization`
  expects, with appropriately configured covariance.
- `odom_publisher_node` (if needed) — any custom processing of raw wheel
  odometry before it's fed into the EKF/UKF.

**Build:** standard `ament_cmake` package, built with `colcon build` as part of
a ROS2 workspace.
