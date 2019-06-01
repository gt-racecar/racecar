#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDriveStamped

def callback(data):

    msg = AckermannDriveStamped();
    msg.header.stamp = rospy.Time.now();
    msg.header.frame_id = "base_link";

    cut = .2
    if (data.linear.x != 0) and (abs(data.linear.x) < cut):
	if data.linear.x < 0:
	    data.linear.x = -1 * cut
	else:
	    data.linear.x = cut


    msg.drive.speed = data.linear.x*1;
    msg.drive.acceleration = 1;#2;
    msg.drive.jerk = 1;#2;

    msg.drive.steering_angle = data.angular.z
    msg.drive.steering_angle_velocity = 1;#2

    pub.publish(msg)

    rospy.loginfo(rospy.get_caller_id() + " linear x: %s", data.linear.x)
    rospy.loginfo(rospy.get_caller_id() + "angular z: %s\n", data.angular.z)

    
def listener():
    rospy.init_node('geo_acker_node', anonymous=True)
    rospy.Subscriber("cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    pub = rospy.Publisher('/vesc/ackermann_cmd_mux/input/navigation', AckermannDriveStamped)
    listener()
