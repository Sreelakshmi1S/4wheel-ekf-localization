# Multi-Sensor Localization of a 4-Wheeled Mobile Robot (ROS2 + Gazebo)

Fusing wheel odometry, IMU, and camera-based fiducial (ArUco) localization with an
Extended/Unscented Kalman Filter, benchmarked against ground truth in simulation.

## Problem Statement

Wheel odometry and IMU-only localization drift over time — small errors in wheel slip,
encoder noise, and IMU bias accumulate without bound. This project builds a 4-wheeled
mobile robot in Gazebo and corrects that drift by fusing:

- **Wheel odometry** — fast, local, but drifts over time.
- **IMU** — high-frequency orientation/angular velocity, but biased and noisy.
- **Camera-based fiducial localization** — ArUco markers at known world positions,
  giving sparse but absolute (non-drifting) pose corrections.

These sources are fused using `robot_localization`'s EKF (and, as a comparison, its
UKF) to produce a single filtered pose estimate, evaluated against Gazebo's
ground-truth pose over a driven trajectory.

**Goal:** quantify how much the fused estimate reduces drift compared to
odometry-only localization, and compare EKF vs. UKF behavior on the same data.

## Tech Stack

- ROS2 Humble (Ubuntu 22.04)
- Gazebo Fortress
- C++ (custom nodes) / Python (analysis & evaluation scripts)
- `robot_localization`, `ros2_aruco` / `aruco_opencv`

## Repository Structure

```
4wheel-ekf-localization/
├── robot_description/    # URDF/Xacro: 4-wheel robot, camera, IMU
├── gazebo_sim/           # World file, ArUco marker models, launch files
├── camera_calibration/   # Simulated camera calibration (distortion recovery)
├── localization_cpp/     # Custom C++ ROS2 nodes (bridge/integration logic)
├── ekf_config/           # robot_localization EKF/UKF parameter YAMLs
├── analysis/             # Trajectory evaluation, RMSE, EKF-vs-UKF plots
└── docs/                 # Environment setup, project notes, findings
```

## Build Log

Working through this one concrete step at a time rather than a fixed upfront plan —
each step below only gets added once the previous one is actually working.

- [x] **Step 1 — Robot appears in Gazebo.** 4-wheel skid-steer URDF/xacro, spawned
      into an empty Gazebo Fortress world via `ros2 launch gazebo_sim
      spawn_robot.launch.py`.
- [ ] **Step 2 — Drive it.** Send `/cmd_vel` commands (one-off `ros2 topic pub` and
      `teleop_twist_keyboard`) and confirm forward/backward/turn-in-place all work,
      and that `/odom` publishes sane values.
- [ ] **Step 3 — TBD**, decided once Step 2 is confirmed working.

## Background

Built as an independent project extending localization/SLAM/state-estimation (EKF,
UKF, camera calibration) work from my M.Sc. coursework at the University of
Stuttgart into a full ROS2 + Gazebo system, and as hands-on practice with C++ in a
ROS2 context alongside my Python-based research work at Fraunhofer IPA.

## Author

Sreelakshmi Sujatha — LinkedIn · GitHub