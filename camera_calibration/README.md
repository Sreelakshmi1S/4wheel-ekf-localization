# camera_calibration

Recovers the intrinsics/distortion of the simulated camera, as an explicit
demonstration of the camera calibration step (Stage 3 in the project plan).

**Approach:**
1. The simulated camera in `robot_description/` is configured with known,
   deliberately-added distortion coefficients (Gazebo cameras are otherwise
   near-ideal, so without this step there's nothing to actually calibrate).
2. A checkerboard calibration target is spawned in the Gazebo world.
3. ROS2's `camera_calibration` node (from `image_pipeline`) is run against
   the simulated camera feed to recover the intrinsics and distortion
   coefficients.

**Contents (to be added):**
- `calibration_result.yaml` — recovered camera intrinsics/distortion
- `comparison.md` — recovered values vs. the ground-truth values configured
  in the URDF/SDF, as the proof-of-work artifact for this stage