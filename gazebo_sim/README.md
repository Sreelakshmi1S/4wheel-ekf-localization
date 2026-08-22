# gazebo_sim

Simulation world and launch files.

**Contents (to be added):**
- `worlds/` — Gazebo world file with ArUco markers placed at known, fixed poses
- `models/` — ArUco marker models (visual planes with marker textures)
- `launch/` — launch files to spawn the robot, bridge topics via `ros_gz_bridge`,
  and bring up the full simulation

**Marker placement:** markers are placed at known world coordinates so their
detected poses can be used as ground-truth-anchored corrections in the EKF/UKF.
