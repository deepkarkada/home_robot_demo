# home_robot_demo

Test environment configuration
| Component | Requirement | 
|---|---|
| OS | Ubuntu 24.04 (Noble) | 
| ROS distribution | ROS 2 Jazzy | 
| Simulator | Gazebo Harmonic | 
| Build system | Colcon | 

### Installation instructions ros2 jazzy and gazebo harmonic:
sudo apt install -y software-properties-common <br>
sudo add-apt-repository universe <br>

sudo apt update && sudo apt install -y curl <br>
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg <br>

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null <br>
sudo apt update <br>
sudo apt upgrade <br>

sudo apt install -y ros-jazzy-desktop ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-sim python3-rosdep python3-colcon-common-extensions <br>

sudo apt install -y ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-controller-manager ros-jazzy-joint-state-broadcaster ros-jazzy-diff-drive-controller ros-jazzy-gz-ros2-control ros-jazzy-robot-state-publisher ros-jazzy-joint-state-publisher ros-jazzy-xacro <br>

source /opt/ros/jazzy/setup.bash <br>

### Build and run
git clone https://github.com/deepkarkada/home_robot_demo.git <br>
cd home_robot_demo/ros2_ws

### Colcon build:
colcon build <br>
source install/setup.bash 

### ROS 2 launch
ros2 launch home_robot_demo demo.launch.py <br>

$${\color{red}Note:}$$ The models of the toys and block are loaded from Gazebo fuel, which might cause delays in loading of the Gazebo UI and errors such as missing textures. This is temporary and did load correctly in my testing. You might also see an error window pop up asking to quit or wait for GUI to load. Just click on wait and it does load correctly.