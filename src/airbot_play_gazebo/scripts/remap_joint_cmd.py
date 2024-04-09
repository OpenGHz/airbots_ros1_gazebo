import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class RemapJointCmd(object):
    def __init__(self, namespace, rate=200):
        self.rate = rate
        source_arm = f"{namespace}/joint_cmd"
        source_gripper = f"{namespace}/end_effector/command"
        target_arm = f"{namespace}/arm_group_position_controller/command"
        target_gripper = (
            f"{namespace}/gripper_group_position_controller/command"
        )

        self.arm_cmd_sub = rospy.Subscriber(
            source_arm, JointState, self.arm_joint_cmd_cb
        )
        self.gripper_cmd_sub = rospy.Subscriber(
            source_gripper, JointState, self.gripper_cmd_cb
        )
        self.arm_cmd_pub = rospy.Publisher(target_arm, Float64MultiArray, queue_size=10)
        self.gripper_cmd_pub = rospy.Publisher(
            target_gripper, Float64MultiArray, queue_size=10
        )

        self.arm_cmd = rospy.wait_for_message(source_arm, JointState)
        self.gripper_cmd = rospy.wait_for_message(source_gripper, JointState)

    def arm_joint_cmd_cb(self, msg: JointState):
        self.arm_cmd = msg
        target_arm_msg = Float64MultiArray()
        target_arm_msg.data = self.arm_cmd.position
        self.arm_cmd_pub.publish(target_arm_msg)

    def gripper_cmd_cb(self, msg: JointState):
        self.gripper_cmd = msg
        target_gripper_msg = Float64MultiArray()
        target_gripper_msg.data = self.gripper_cmd.position
        self.gripper_cmd_pub.publish(target_gripper_msg)

    def run(self):
        rate = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            target_arm_msg = Float64MultiArray()
            target_gripper_msg = Float64MultiArray()
            target_arm_msg.data = self.arm_cmd.position
            target_gripper_msg.data = self.gripper_cmd.position
            self.arm_cmd_pub.publish(target_arm_msg)
            self.gripper_cmd_pub.publish(target_gripper_msg)
            rate.sleep()


if __name__ == "__main__":
    rospy.init_node("remap_joint_cmd")
    namespace = rospy.get_namespace()
    remap_joint_cmd = RemapJointCmd(namespace)
    # remap_joint_cmd.run()
    rospy.spin()
