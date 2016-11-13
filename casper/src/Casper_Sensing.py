#!/usr/bin/env python
# license removed for brevity
import rospy
from casper.msg import sensorList

def Casper_Sensing():
    pub = rospy.Publisher('Sensing_Results', sensorList, queue_size=10)
    rospy.init_node('Casper_Sensing', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg = sensorList()
    msg.sensor = "Touch"
    msg.sensor_type = 3
    while not rospy.is_shutdown():
       # rospy.loginfo(sensorList)
       pub.publish(msg)
       rate.sleep()

if __name__ == '__main__':
    try:
        Casper_Sensing()
    except rospy.ROSInterruptException:
        pass
