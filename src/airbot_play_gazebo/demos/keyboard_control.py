import rospy
from airbot_play_control.control import RoboticArmAgent, AirbotPlayConfig
from moveit_commander import MoveGroupCommander

NODE_NAME = 'airbot_play_gazebo'
rospy.init_node(NODE_NAME)

other_config=("", "airbot_play_arm")
airbot_play_arm = RoboticArmAgent(control_mode=AirbotPlayConfig.normal,init_pose=3,
                      node_name=NODE_NAME,other_config=other_config)
airbot_play_gripper = MoveGroupCommander("airbot_play_gripper")
airbot_play_gripper.set_max_acceleration_scaling_factor(0.1)
airbot_play_gripper.set_max_acceleration_scaling_factor(0.1)

grasp_state = False
while airbot_play_arm.is_alive():
    key = airbot_play_arm.key_control(delta_task=0.005,disable_keys=['p'],instruction=True)
    if (key == 'p'):
        if not grasp_state:
            airbot_play_gripper.set_named_target("pick_big_cube")
            airbot_play_gripper.go()
        else:
            airbot_play_gripper.set_named_target("open")
            airbot_play_gripper.go()
        grasp_state = ~grasp_state