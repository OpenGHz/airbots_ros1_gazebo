#!/bin/bash

current_dir=$(pwd)

if [ -n "$GAZEBO_RESOURCE_PATH" ];then  # the GAZEBO_RESOURCE_PATH is not empty showing the gazebo has been configured
    if [[ $GAZEBO_RESOURCE_PATH == *"airbot_play_gazebo"* ]];then
        new_config="export GAZEBO_RESOURCE_PATH=${current_dir}":'"$GAZEBO_RESOURCE_PATH"'
        # sed -i "/airbot_play_gazebo/d" ~/."${SHELL##*/}"rc  # remove the old config in the rc file
        sed -i "/airbot_play_gazebo/c\\${new_config}" ~/."${SHELL##*/}"rc
    else
        echo "export GAZEBO_RESOURCE_PATH=${current_dir}":'"$GAZEBO_RESOURCE_PATH"' >> ~/."${SHELL##*/}"rc
    fi
    GAZEBO_RESOURCE_PATH=${current_dir}:$GAZEBO_RESOURCE_PATH && export GAZEBO_RESOURCE_PATH
else
    echo "export GAZEBO_RESOURCE_PATH=${current_dir}" >> ~/."${SHELL##*/}"rc
    GAZEBO_RESOURCE_PATH=${current_dir} && export GAZEBO_RESOURCE_PATH
    # source the gazebo setup.bash file
    echo 'current_dir=$(pwd) && cd /usr/share/gazebo-*/ && source setup.bash && cd ${current_dir} && unset current_dir' >> ~/."${SHELL##*/}"rc
    cd /usr/share/gazebo-*/ && source setup.bash && cd "$current_dir"
fi

# echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:${current_dir}/models" >> ~/."${SHELL##*/}"rc

# OK
echo -e "\e[1;32mGazebo config OK.\e[0m"