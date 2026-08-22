# Multi-Sensor Localization of a 4-Wheeled Mobile Robot (ROS2 + Gazebo)

Fusing wheel odometry, IMU, and camera-based fiducial (ArUco) localization with an
Extended/Unscented Kalman Filter, benchmarked against ground truth in simulation.

> **Status:** 🚧 In progress. See [Roadmap](#roadmap) for current stage.

## Problem Statement

Wheel odometry and IMU-only localization drift over time — small errors in wheel
slip, encoder noise, and IMU bias accumulate without bound. This project builds a
4-wheeled mobile robot in Gazebo and corrects that drift by fusing:

1. **Wheel odometry** — fast, local, but drifts over time.
2. **IMU** — high-frequency orientation/angular velocity, but biased and noisy.
3. **Camera-based fiducial localization** — ArUco markers at known world positions,
   giving sparse but *absolute* (non-drifting) pose corrections.

These three sources are fused using `robot_localization`'s EKF (and, as a
comparison, its UKF) to produce a single filtered pose estimate, which is then
evaluated against Gazebo's ground-truth pose over a driven trajectory.

**Goal:** quantify how much the fused estimate reduces drift compared to
odometry-only localization, and compare EKF vs. UKF behavior on the same data.

## Why This Setup

| Component | Role | Package |
|---|---|---|
| Wheel odometry | Continuous local motion estimate | Gazebo differential/skid-steer plugin via `ros_gz` |
| IMU | High-rate orientation correction | Gazebo IMU sensor plugin |
| Camera + ArUco markers | Absolute pose correction (anchors the drift) | [`ros2_aruco`](https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco) or [`aruco_opencv`](https://github.com/fictionlab/ros_aruco_opencv) |
| Sensor fusion | EKF / UKF state estimation | [`robot_localization`](https://github.com/cra-ros-pkg/robot_localization) |
| Simulation | Physics, sensors, ground truth | Gazebo (modern, via `ros_gz_bridge`) |
| Integration nodes | Bridging marker detections into `robot_localization`'s expected input, custom odometry handling | Custom C++ (`localization_cpp/`) |

The filter math itself uses the field-standard `robot_localization` package rather
than a from-scratch reimplementation — the goal of this project is demonstrating
correct **integration, system design, and evaluation** of a real localization
stack, which is the actual day-to-day work in robotics software roles. A
from-scratch EKF derivation (Python) is included separately in `analysis/` as a
supplementary piece showing the underlying math is understood, not just used as
a black box.

## Repository Structure

```
4wheel-ekf-localization/
├── robot_description/     # URDF/Xacro: 4-wheel robot, camera, IMU
├── gazebo_sim/             # World file, ArUco marker models, launch files
├── localization_cpp/       # Custom C++ ROS2 nodes (bridge/integration logic)
├── ekf_config/              # robot_localization EKF/UKF parameter YAMLs
├── analysis/                 # Trajectory evaluation, RMSE, EKF-vs-UKF plots
└── docs/                      # Results write-up, plots, findings
```

## Tech Stack

- **ROS2** (Jazzy)
- **Gazebo** (modern, `ros_gz` — not Gazebo Classic)
- **C++** (custom nodes) / **Python** (analysis & evaluation scripts)
- `robot_localization`, `ros2_aruco` / `aruco_opencv`

## Roadmap

- [ ] Stage 1 — URDF for 4-wheeled robot + camera + IMU, spawn and drive in Gazebo
- [ ] Stage 2 — ArUco markers placed in world; verify marker pose detection
- [ ] Stage 3 — `robot_localization` EKF configured, fusing odom + IMU + marker poses; custom C++ bridge node
- [ ] Stage 4 — UKF comparison run
- [ ] Stage 5 — Evaluation: ground truth vs. odom-only vs. EKF vs. UKF trajectories, RMSE, write-up in `docs/`

## Results

_Coming soon — trajectory plots and drift-reduction numbers will be added here
once Stage 5 is complete._

## Background

Built as an independent project extending localization/SLAM/state-estimation
(EKF, UKF, camera calibration) work from my M.Sc. coursework at the University
of Stuttgart into a full ROS2 + Gazebo system, and as hands-on practice with
C++ in a ROS2 context alongside my Python-based research work at Fraunhofer IPA.

## Author

Sreelakshmi Sujatha — [LinkedIn](https://www.linkedin.com/in/sreelakshmi-sujatha) · [GitHub](https://github.com/Sreelakshmi1S)
