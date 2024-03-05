#!/usr/bin/env bash

# install necessary packages
sudo apt-get install \
    ros-"$ROS_DISTRO"-gazebo-ros \
    ros-"$ROS_DISTRO"-eigen-conversions \
    ros-"$ROS_DISTRO"-object-recognition-msgs \
    ros-"$ROS_DISTRO"-roslint

# OK
echo -e "\e[1;32mGrasp plugin config OK.\e[0m"