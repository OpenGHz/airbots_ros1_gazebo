```bash

pushd src/airbot_play_gazebo

chmod +x *.sh
sudo apt install ros-noetic-gazebo-plugins
./gazebo_config.sh
./gazebo_grasp_config.sh
./download_models.sh

source devel/setup.bash

```