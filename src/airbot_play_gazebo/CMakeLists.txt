cmake_minimum_required(VERSION 2.8.3)

cmake_policy(SET CMP0048 NEW)

project(airbot_play_gazebo)

find_package(catkin REQUIRED COMPONENTS
  gazebo_plugins
  gazebo_ros
  gazebo_ros_control
  urdf
  xacro
)
catkin_package()

find_package(roslaunch)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config)

catkin_install_python(PROGRAMS
  demos/keyboard_control.py
  scripts/remap_joint_cmd.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)