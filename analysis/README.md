# analysis

Evaluation scripts comparing localization approaches.

**Planned contents:**
- `evaluate_trajectory.py` — logs ground truth (from Gazebo), raw odometry, and
  filtered EKF/UKF output over a driven trajectory; computes position/orientation
  RMSE for each against ground truth; produces comparison plots.
- `ekf_from_scratch.py` (supplementary) — a minimal from-scratch EKF
  implementation on the same logged sensor data, to demonstrate understanding
  of the underlying filter math independent of `robot_localization`'s
  implementation.

**Metrics to report:**
- Position RMSE (odometry-only vs. EKF-fused vs. UKF-fused)
- Orientation RMSE
- Qualitative drift comparison over trajectory length
