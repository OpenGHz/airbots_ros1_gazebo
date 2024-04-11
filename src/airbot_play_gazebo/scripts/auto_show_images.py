import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from typing import List, Any


class ImageAutoShower:
    #TODO: need fix
    def __init__(self):
        self.bridge = CvBridge()
        self.images = {}  # 保存接收到的图像

        # 订阅所有话题
        self.subscribers = {}
        self.subscribe_topics()

    def subscribe_topics(self):
        # 获取所有话题列表
        topics:List[List[str, Any]] = rospy.get_published_topics()
        for topic, topic_type in topics:
            # 判断话题名中是否包含 "image" 或 "camera"，并且类型是否为 Image
            if ("image" in topic.lower() or "camera" in topic.lower()) and topic_type == "sensor_msgs/Image":
                image = rospy.wait_for_message(topic, Image, timeout=5)
                self.images[topic] = self.bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
                self.subscribers[topic] = rospy.Subscriber(topic, Image, self.image_callback, callback_args=topic)

    def image_callback(self, msg, topic):
        # 将 ROS 图像消息转换为 OpenCV 格式
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self.images[topic] = cv_image

    def display_images(self):
        while not rospy.is_shutdown():
            # 将所有图像拼接成一张大图
            stitched_image = np.hstack(list(self.images.values()))
            cv2.imshow("Stitched Image", stitched_image)
            cv2.waitKey(1)


if __name__ == "__main__":
    rospy.init_node("image_processor")
    image_processor = ImageAutoShower()
    image_processor.display_images()