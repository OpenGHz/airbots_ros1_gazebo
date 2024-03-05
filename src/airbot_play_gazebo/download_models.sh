#!/usr/bin/env bash

set -e

# check whether models have been downloaded
if [ -d "~/.gazebo/models" ];then
    echo "Models have already been downloaded."
    exit 0
fi

# if [ -n "$GAZEBO_MODEL_PATH" ];then
#     if [[ $GAZEBO_MODEL_PATH == *"airbot_play_gazebo"* ]];then
#         echo "Gazebo model path has been configured."
#     else
#         echo "export GAZEBO_MODEL_PATH=${current_dir}/models":'$GAZEBO_MODEL_PATH' >> ~/."${SHELL##*/}"rc
#     fi
# else
#     echo "export GAZEBO_MODEL_PATH=${current_dir}/models" >> ~/."${SHELL##*/}"rc
# fi

mkdir ~/.gazebo/models
pushd ~/.gazebo/models > /dev/null

wget http://file.ncnynl.com/ros/gazebo_models.txt
wget -i gazebo_models.txt

ls model.tar.g* | xargs -n1 tar xzvf

popd > /dev/null
