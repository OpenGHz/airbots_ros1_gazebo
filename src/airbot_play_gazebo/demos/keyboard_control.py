import rospy
from airbot_play_control.control import RoboticArmAgent, AirbotPlayConfig
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import PoseStamped


NODE_NAME = 'airbot_play_gazebo_keyboard'
rospy.init_node(NODE_NAME)

other_config=("", "airbot_play_arm")
# other_config = None
airbot_play_arm = RoboticArmAgent(control_mode=AirbotPlayConfig.normal,init_pose=None,
                      node_name=NODE_NAME,other_config=other_config)
# airbot_play_arm.set_and_go_to_pose_target([0.702,-0.17,0.614],[0,0,0,1])
airbot_play_arm.set_and_go_to_pose_target([0.65,-0.11,0.47],[0,1.5708,0])
airbot_play_gripper = MoveGroupCommander("airbot_play_gripper")
airbot_play_gripper.set_max_acceleration_scaling_factor(0.1)
airbot_play_gripper.set_max_acceleration_scaling_factor(0.1)

# 发布末端位姿话题
eef_pose_pub = rospy.Publisher("/airbot_play/current_pose", PoseStamped, queue_size=1)
def publish_eef_pose():
    rt = rospy.Rate(200)
    while True:
        eef_pose =  airbot_play_arm.arm_moveit.get_current_pose()
        eef_pose_pub.publish(eef_pose)
        rt.sleep()
from threading import Thread
Thread(target=publish_eef_pose,daemon=True).start()

grasp_state = True
def pick():
    global grasp_state
    if not grasp_state:
        # 夹爪闭合
        SCALE_CLOSE = 0.7
        delta = 0.04
        CLOSE = (-SCALE_CLOSE,SCALE_CLOSE,SCALE_CLOSE,-SCALE_CLOSE + delta)
        airbot_play_gripper.go(CLOSE)
    else:
        airbot_play_gripper.set_named_target("open")
        airbot_play_gripper.go()
    grasp_state = not grasp_state

pick()
while airbot_play_arm.is_alive():
    key = airbot_play_arm.key_control(delta_task=0.005,disable_keys=['p'],instruction=True)
    if key == 'p':
        pick()
    # elif key == '*':
    #     airbot_play_arm.go_to_named_or_joint_target('Home')
    # elif key == '/':
    #     airbot_play_arm.set_and_go_to_pose_target([0.65,-0.11,0.47],[0,1.5708,0])