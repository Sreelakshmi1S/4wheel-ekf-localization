# robot_description

URDF/Xacro description of the 4-wheeled robot used in this project.

**Contents (to be added):**
- `urdf/` — robot URDF/Xacro: chassis, 4 wheels, IMU link, camera link
- `meshes/` — any visual meshes (optional; primitive shapes are fine for this project)

**Sensors modeled:**
- IMU (Gazebo IMU plugin)
- Camera (Gazebo camera plugin, for ArUco detection)
- Wheel odometry (via Gazebo diff-drive / skid-steer plugin)
