# Four-Wheel Robot Localization and SLAM

> **Status:** Work in progress  
> **Environment:** ROS 2 Humble, Gazebo Fortress, Ubuntu 22.04

A simulation project for exploring localization, sensor fusion, and SLAM with a four-wheel skid-steer robot.

The robot model will be adapted from Linorobot2 for Gazebo Fortress. Existing ROS 2 packages will provide standard infrastructure, while the core localization and evaluation components will be implemented in C++.

## Goals

- Simulate a four-wheel robot with wheel encoders, IMU, camera, and 2D LiDAR.
- Implement wheel odometry in C++.
- Fuse odometry, IMU, and ArUco observations using EKF and UKF.
- Implement and test a custom planar EKF in C++.
- Compare the custom estimator with `robot_localization`.
- Integrate SLAM Toolbox for LiDAR SLAM.
- Evaluate estimates against Gazebo ground truth.

## Planned Experiments

The estimators will be tested using repeatable trajectories under:

- wheel slip and encoder noise;
- IMU noise and bias;
- missing fiducial observations;
- measurement outliers;
- sensor delays and dropouts.

Evaluation will include position error, heading error, final drift, and recovery after absolute pose corrections.

## Technology

- ROS 2 Humble
- Gazebo Fortress and `ros_gz`
- C++17 and Eigen
- Python for analysis and plotting
- `robot_localization`
- SLAM Toolbox
- Nav2
- ArUco or AprilTag detection

## Progress

- [X] Adapt a four-wheel Linorobot2 model for Gazebo Fortress
- [ ] Validate driving, joint states, TF, and wheel odometry
- [ ] Add IMU, camera, LiDAR, and ground truth
- [ ] Implement custom wheel odometry in C++
- [ ] Implement fiducial-based global localization in C++
- [ ] Configure `robot_localization` EKF and UKF
- [ ] Implement and test a custom planar EKF in C++
- [ ] Integrate SLAM Toolbox and Nav2
- [ ] Run controlled experiments and publish results

## Reuse and Attribution

The robot description and selected simulation assets are adapted from
[Linorobot2](https://github.com/linorobot/linorobot2).

Third-party components retain their original licences and attribution. Reused
files and modifications will be documented separately.

## Background

This project extends my M.Sc. work in state estimation, localization, SLAM,
and camera calibration into a complete ROS 2 simulation. It also serves as a
practical demonstration of C++, ROS 2 integration, testing, and quantitative
validation.

## Author

Sreelakshmi Sujatha

