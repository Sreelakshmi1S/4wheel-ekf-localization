# Environment Setup — Ubuntu 22.04 + ROS2 Humble + Gazebo Fortress

This project targets **Ubuntu 22.04 (Jammy)**, **ROS2 Humble**, and **Gazebo Fortress**
(the officially-supported pairing for Humble). All commands below are run on the
host machine, in a normal terminal.

## 1. C++ build tools

```bash
sudo apt update
sudo apt install -y build-essential cmake git
```

## 2. Locale (ROS2 needs UTF-8)

```bash
sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
```
Open a new terminal after this.

## 3. Enable apt sources

```bash
sudo apt install -y software-properties-common
sudo add-apt-repository universe
```

Then add the ROS2 apt repo using the **current officially-supported method**
(`ros2-apt-source`), not the older manual `apt-key`/keyserver method — that older
method is deprecated and commonly fails with a `NO_PUBKEY F42ED6FBAB17C654` error
on `apt update`.

```bash
# remove any stale/broken ROS2 source file from a previous attempt
sudo rm -f /etc/apt/sources.list.d/ros2*.list

sudo apt update && sudo apt install -y curl

export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

sudo apt update
```

`ros2-apt-source` installs the correct signing key into a proper keyring location
and writes the sources.list entry for you — this is the same fix referenced by
`sudo apt remove ros2-apt-source` in the official uninstall docs, i.e. it's the
current standard, not a workaround.

If `apt update` still complains about `packages.osrfoundation.org` using a
"legacy trusted.gpg keyring" — that one's just a deprecation *warning* (`W:`, not
`E:`), it won't block installs. Safe to ignore for now.

## 4. Install ROS2 Humble

```bash
sudo apt update
sudo apt install -y ros-humble-desktop ros-dev-tools
```

`ros-humble-desktop` includes rclcpp, rviz2, robot_state_publisher, etc.
`ros-dev-tools` gives you colcon, rosdep, and friends.

## 5. Install Gazebo Fortress + ROS2 bridge packages

```bash
sudo apt install -y ros-humble-ros-gz ros-humble-xacro ros-humble-teleop-twist-keyboard
```

`ros-humble-ros-gz` is the meta-package that pulls in Gazebo Fortress itself plus
`ros_gz_sim` / `ros_gz_bridge` — no extra OSRF repo needed, since Fortress is
Humble's officially supported Gazebo version.

## 6. Source ROS2 in every new shell

```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

## 7. Create your colcon workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

## 8. Verify

```bash
ros2 --version
gz sim --version || ign gazebo --version
ros2 pkg list | grep ros_gz
```

All three should return sensible output with no errors. If `gz sim` isn't found
but `ign gazebo` is, that's expected on Fortress — use whichever the install
provides; the launch files in `gazebo_sim/` go through `ros2 launch ros_gz_sim
gz_sim.launch.py`, which works either way.

## 9. Drop the packages in and build

```bash
cd ~/ros2_ws/src
# copy or clone robot_description/ and gazebo_sim/ in here
cd ~/ros2_ws
colcon build --packages-select robot_description gazebo_sim
source install/setup.bash
ros2 launch gazebo_sim spawn_robot.launch.py
```

## Version note

The original project plan targeted ROS2 Jazzy + Gazebo Harmonic (Ubuntu 24.04).
The dev machine is on 22.04, so this project uses Humble + Fortress instead — the
officially-supported pairing, versus running Harmonic on Humble unofficially via
extra OSRF packages. The only concrete differences that show up in code:

- SDF/URDF plugin filenames and C++ namespaces use `ignition::gazebo::systems::*`
  (Fortress) instead of `gz::sim::systems::*` (Harmonic).
- `ros_gz_bridge` message types use the `ignition.msgs.*` namespace instead of
  `gz.msgs.*`.
- ROS package names (`ros_gz_sim`, `ros_gz_bridge`, `xacro`, etc.) are unchanged.
