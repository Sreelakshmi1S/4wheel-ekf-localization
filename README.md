# Multi-Sensor Localization of a 4-Wheeled Mobile Robot (ROS2 + Gazebo)

Fusing wheel odometry, IMU, and camera-based fiducial (ArUco) localization with an
Extended/Unscented Kalman Filter, benchmarked against ground truth in simulation.

> **Status:** 🚧 In progress. See [Roadmap](#roadmap) for current stage.

## Problem Statement

Wheel odometry and IMU-only localization drift over time — small errors in wheel slip,
encoder noise, and IMU bias accumulate without bound. This project builds a 4-wheeled
mobile robot in Gazebo and corrects that drift by fusing:

- **Wheel odometry** — fast, local, but drifts over time.
- **IMU** — high-frequency orientation/angular velocity, but biased and noisy.
- **Camera-based fiducial localization** — ArUco markers at known world positions,
  giving sparse but absolute (non-drifting) pose corrections.

These three sources are fused using `robot_localization`'s EKF (and, as a comparison,
its UKF) to produce a single filtered pose estimate, which is then evaluated against
Gazebo's ground-truth pose over a driven trajectory.

**Goal:** quantify how much the fused estimate reduces drift compared to
odometry-only localization, and compare EKF vs. UKF behavior on the same data.

## Why This Setup

| Component | Role | Package |
|---|---|---|
| Wheel odometry | Continuous local motion estimate | Gazebo differential drive plugin(s) via `ros_gz` |
| IMU | High-rate orientation correction | Gazebo IMU sensor plugin |
| Camera calibration | Recovering intrinsics/distortion from the simulated camera | ROS2 `camera_calibration` (`image_pipeline`) |
| Camera + ArUco markers | Absolute pose correction (anchors the drift) | `ros2_aruco` |
| Sensor fusion | EKF / UKF state estimation | `robot_localization` |
| Simulation | Physics, sensors, ground truth | Gazebo Harmonic (via `ros_gz_bridge`) |
| Integration nodes | Bridging marker detections into `robot_localization`'s expected input, custom odometry handling | Custom C++ (`localization_cpp/`) |
| Multi-camera fusion (stretch) | Handing off marker corrections between multiple fixed cameras | Extension of `localization_cpp/` |

The filter math itself uses the field-standard `robot_localization` package rather
than a from-scratch reimplementation — the goal of this project is demonstrating
correct integration, system design, and evaluation of a real localization stack,
which is the actual day-to-day work in robotics software roles. A from-scratch EKF
derivation (Python) is included separately in `analysis/` as a supplementary piece
showing the underlying math is understood, not just used as a black box.

## Repository Structure

```
4wheel-ekf-localization/
├── robot_description/   # URDF/Xacro: 4-wheel robot, camera, IMU
├── gazebo_sim/           # World file, ArUco marker models, launch files
├── camera_calibration/   # Simulated camera calibration (distortion recovery)
├── localization_cpp/     # Custom C++ ROS2 nodes (bridge/integration logic)
├── ekf_config/            # robot_localization EKF/UKF parameter YAMLs
├── analysis/               # Trajectory evaluation, RMSE, EKF-vs-UKF plots
└── docs/                     # Project plan, results write-up, plots, findings
```

## Attribution

The Stage 1 robot/world setup follows the structure taught in the MOGI-ROS
Week-3-4-Gazebo-basics course material (Apache-2.0, public teaching material) —
package naming, robot dimensions, and inertia values here are my own rather than
the tutorial's example figures. Everything from sensor fusion onward (camera
calibration, ArUco-corrected EKF/UKF, evaluation) is original integration work not
covered by that or any single tutorial. Full breakdown in `docs/project-plan.md`.

## Tech Stack

- ROS2 (Jazzy)
- Gazebo (modern, `ros_gz` — not Gazebo Classic)
- C++ (custom nodes) / Python (analysis & evaluation scripts)
- `robot_localization`, `ros2_aruco` / `aruco_opencv`

## Roadmap

- [x] **Stage 1a** — URDF for a bare 4-wheeled skid-steer chassis, spawned in an
      empty Gazebo world, driveable via `/cmd_vel` (no sensors yet)
- [ ] **Stage 1b** — Add IMU and camera links/sensors to the URDF; verify both
      publish in Gazebo
- [ ] **Stage 2** — Camera calibration: recover distortion coefficients from the
      simulated camera
- [ ] **Stage 3** — ArUco markers placed in world; verify marker pose detection
- [ ] **Stage 4** — `robot_localization` EKF configured, fusing odom + IMU + marker
      poses; custom C++ bridge node
- [ ] **Stage 5** — UKF comparison run
- [ ] **Stage 6** — Evaluation: ground truth vs. odom-only vs. EKF vs. UKF
      trajectories, RMSE, write-up in `docs/`
- [ ] **Stage 7 (stretch)** — Multi-camera localization

Full detail on each stage, including "done when" criteria and resources:
`docs/project-plan.md`.

## Getting Started (Stage 1a)

Requires ROS2 Jazzy and Gazebo Harmonic (`ros_gz`) already installed and sourced.

```bash
# from your colcon workspace src/ folder
cd ~/ros2_ws/src
# copy/clone robot_description/ and gazebo_sim/ in here

cd ~/ros2_ws
colcon build --packages-select robot_description gazebo_sim
source install/setup.bash

ros2 launch gazebo_sim spawn_robot.launch.py
```

Gazebo should open with the robot sitting on the ground plane. Drive it:

```bash
# one-off nudge forward
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}"

# interactive keyboard teleop (install if missing: sudo apt install ros-jazzy-teleop-twist-keyboard)
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Check odometry is being published:

```bash
ros2 topic echo /odom
```

Once forward/backward/turn-in-place all behave as expected, Stage 1a is done and
we move on to adding the IMU and camera in Stage 1b.

## Results

Coming soon — trajectory plots and drift-reduction numbers will be added here once
Stage 6 is complete.

## Background

Built as an independent project extending localization/SLAM/state-estimation (EKF,
UKF, camera calibration) work from my M.Sc. coursework at the University of
Stuttgart into a full ROS2 + Gazebo system, and as hands-on practice with C++ in a
ROS2 context alongside my Python-based research work at Fraunhofer IPA.

## Author

Sreelakshmi Sujatha — LinkedIn · GitHub