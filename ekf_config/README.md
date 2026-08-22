# ekf_config

`robot_localization` parameter files.

**Contents (to be added):**
- `ekf.yaml` — EKF node configuration: sensor inputs (odom, IMU, marker pose),
  which state variables each sensor updates, process noise covariance
- `ukf.yaml` — equivalent UKF configuration, for the EKF vs. UKF comparison

Both filters will be run on identical sensor input data so the comparison in
`analysis/` isolates the effect of the filtering algorithm itself.
