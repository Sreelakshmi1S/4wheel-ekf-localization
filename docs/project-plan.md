# Project Plan

A working plan for building this project, with concrete external resources
for each stage.

## Attribution & Originality

The robot/world setup in Stage 1 is built following the structure and Gazebo
plugin configuration taught in the [MOGI-ROS Week-3-4-Gazebo-basics course
material](https://github.com/MOGI-ROS/Week-3-4-Gazebo-basics) (Apache-2.0
licensed, public teaching material). This project uses its own package
naming, robot dimensions, mass, and derived inertia values rather than
reusing the tutorial's example figures directly.

Everything from Stage 4 onward — fusing ArUco marker corrections into
`robot_localization`, the EKF/UKF comparison, the camera calibration
procedure, and the quantitative evaluation — is original integration work
not covered by any single tutorial; it combines several standard ROS2
packages (`robot_localization`, `ros2_aruco`, `camera_calibration`) into a
working, evaluated pipeline.

## Primary learning resource

The [MOGI-ROS course series](https://github.com/MOGI-ROS) (BME) is the
backbone learning reference for this project. It's actively maintained, uses
**ROS2 Jazzy + Gazebo Harmonic** (matches this project's stack exactly), and
is structured as weekly modules with a `starter-branch` to build from.

| Module | Covers | Relevant to |
|---|---|---|
| [Week-1-2-Introduction-to-ROS2](https://github.com/MOGI-ROS/Week-1-2-Introduction-to-ROS2) | ROS2 pub/sub basics (C++ & Python) | Refresher / C++ node structure |
| [Week-3-4-Gazebo-basics](https://github.com/MOGI-ROS/Week-3-4-Gazebo-basics) | URDF from scratch → 4-wheel skid-steer robot in Gazebo Harmonic | `robot_description/`, `gazebo_sim/` |
| [Week-5-6-Gazebo-sensors](https://github.com/MOGI-ROS/Week-5-6-Gazebo-sensors) | Adding IMU, camera, depth camera, GPS | Sensor setup on the URDF |
| [Week-7-8-ROS2-Navigation](https://github.com/MOGI-ROS/Week-7-8-ROS2-Navigation) | `robot_localization` EKF (odom+IMU fusion), SLAM Toolbox, AMCL | `ekf_config/`, ground-truth/drift evaluation |

## Supporting resources

- **[`ros2_aruco`](https://github.com/JMU-ROBOTICS-VIVA/ros2_aruco)** — ArUco marker detection/pose package, tested on Jazzy. Camera-localization piece.
- **[automaticaddison.com — "Sensor Fusion and Robot Localization Using ROS 2 Jazzy"](https://automaticaddison.com/sensor-fusion-and-robot-localization-using-ros-2-jazzy/)** — hands-on `robot_localization` EKF walkthrough.
- **[automaticaddison.com — "Estimate ArUco Marker Pose Using OpenCV, Gazebo, and ROS 2"](https://automaticaddison.com/estimate-aruco-marker-pose-using-opencv-gazebo-and-ros-2/)** — ArUco + Gazebo + ROS2, step by step.
- **[`robot_localization` official repo](https://github.com/cra-ros-pkg/robot_localization)** — authoritative parameter reference for `ekf.yaml` / `ukf.yaml`.
- **[`camera_calibration` (ROS `image_pipeline`)](https://github.com/ros-perception/image_pipeline)** — standard ROS2 monocular camera calibration tool, used in Stage 3.
- **[`linorobot2`](https://github.com/linorobot/linorobot2)** — full reference implementation (2WD/4WD/Mecanum, `robot_localization` + Nav2 + SLAM Toolbox pre-wired). Use only as a sanity-check reference once your own setup works, not as a source to copy from.

## Known gotcha

`libgazebo_ros_skid_steer_drive` (the "true" 4-wheel independent skid-steer
plugin) has a history of being unreliable — multiple reference projects
mention this. The common, more robust workaround: run **two
differential-drive plugins**, one controlling the front axle pair and one
the rear axle pair, instead of relying on the skid-steer plugin directly.
Decide on this upfront rather than debugging the flaky plugin mid-project.

## Stage-by-Stage Plan

### Stage 1 — Robot + world in Gazebo
- Build URDF/Xacro for a 4-wheeled robot (chassis + 4 wheels + camera link +
  IMU link), following Week-3-4-Gazebo-basics for structure — but with your
  own package name, robot name, dimensions, and derived inertia values (see
  Attribution note above).
- Decide on drive approach now (two diff-drive plugins, front/rear — see
  gotcha above).
- Spawn in an empty Gazebo Harmonic world, verify teleop driving works via
  `ros_gz_bridge`.
- **Done when:** you can drive the robot around an empty world with
  `teleop_twist_keyboard` and see it move correctly in both Gazebo and RViz.

### Stage 2 — Sensors
- Add IMU and camera to the URDF, following Week-5-6-Gazebo-sensors.
- Verify `/imu/data` and `/camera/image_raw` (+ `/camera/camera_info`)
  topics publish correctly.
- **Done when:** `ros2 topic echo` shows sane IMU and camera data while
  driving.

### Stage 3 — Camera calibration
- Deliberately add lens distortion parameters (`k1`, `k2`, `k3`, `p1`, `p2`)
  to the simulated camera in the URDF/SDF, so there's real distortion to
  recover.
- Spawn a checkerboard calibration target model in the world.
- Run ROS2's `camera_calibration` node (from `image_pipeline`) against the
  simulated camera to recover the intrinsics and distortion coefficients.
- Save the calibration result to `camera_calibration/` and compare the
  recovered distortion coefficients against the ground-truth values you set
  — this comparison is the actual proof-of-work artifact for this stage.
- **Done when:** calibration converges and the recovered coefficients are
  reasonably close to the ground truth values you configured.

### Stage 4 — World markers + detection
- Build a Gazebo world with ArUco markers placed at known, fixed world
  coordinates (a few, spaced around a driving loop).
- Bring up `ros2_aruco` using the calibrated camera intrinsics from Stage 3,
  verify marker poses publish relative to the camera frame when markers are
  in view.
- **Done when:** marker detections show up reliably as the robot drives
  past them.

### Stage 5 — Sensor fusion (EKF)
- Configure `robot_localization`'s `ekf_node` (`ekf_config/ekf.yaml`) to
  fuse wheel odom + IMU, following Week-7-8-ROS2-Navigation as the starting
  template.
- Write the custom C++ bridge node (`localization_cpp/`) that converts
  `ros2_aruco` marker detections into the `geometry_msgs/PoseWithCovarianceStamped`
  format `robot_localization` expects as an additional absolute-pose input.
- **Done when:** `/odometry/filtered` tracks the robot's true path more
  closely than raw odometry alone, visibly correcting when a marker comes
  into view.

### Stage 6 — UKF comparison
- Duplicate the EKF config as a UKF config (`ekf_config/ukf.yaml`), same
  sensor inputs.
- Run both filters on the same driven trajectory (either two separate runs
  or, if feasible, logged/replayed sensor data for a fair comparison).
- **Done when:** you have filtered output from both, ready to evaluate.

### Stage 7 — Evaluation & write-up
- `analysis/evaluate_trajectory.py`: log ground truth (Gazebo), raw
  odometry, EKF output, UKF output over a driven loop.
- Compute position/orientation RMSE for each against ground truth; plot
  trajectories overlaid.
- Write `docs/results.md`: plots, RMSE table, a short discussion of EKF vs.
  UKF behavior and how much the camera corrections reduced drift vs.
  odometry-only.
- **Done when:** README's "Results" section links to a clear plot and 2-3
  sentence summary of findings.

### Stage 8 — Multi-camera localization (stretch goal)
- Add a second fixed camera covering a different section of the driving
  loop (e.g. two cameras covering opposite ends), each running its own
  `ros2_aruco` instance.
- Extend the C++ bridge node to handle marker detections from either camera
  frame, transforming each into the robot's world frame correctly before
  publishing to `robot_localization`.
- Handle the case where a marker is briefly visible to both cameras
  simultaneously (either fuse both observations or prioritize the more
  confident one).
- **Done when:** the fused estimate correctly uses corrections from
  whichever camera currently has a marker in view, without discontinuities
  when handing off between cameras.
- **Note:** this stage is what completes the "multi-camera localization"
  claim on the CV — treat Stages 1–7 as the core deliverable, and this as a
  clearly-labeled extension once that's solid, not a blocker to finishing
  the core project.

## Definition of Done (core project, Stages 1–7)

- Robot drives in Gazebo, sensors publish correctly.
- Camera calibration recovers known-good intrinsics/distortion from a
  deliberately-distorted simulated camera.
- EKF and UKF both fuse odom + IMU + ArUco marker corrections.
- Quantitative comparison (RMSE) of odom-only vs. EKF vs. UKF against ground
  truth.
- README results section with a plot and a few sentences of findings — this
  is what a reviewer will actually look at first, so don't skip it even if
  the rest is polished.