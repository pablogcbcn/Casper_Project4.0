#!/usr/bin/env python
# license removed for brevity
import rospy
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention

def Casper_Sensing():

    pub = rospy.Publisher('Sensing_Results', Sensing, queue_size=10)
    rospy.init_node('Casper_Sensing', anonymous=True)
   
    #Casper_Sensing publishing
    rospy.loginfo("publishing to topic Sensing_Results")
    rate = rospy.Rate(10) # 10hz
    sensing_msg = Sensing()
    sensing_msg.sensor = "Banananaaaaa"
    
    while not rospy.is_shutdown():
       pub.publish(sensing_msg)
       rate.sleep()

if __name__ == '__main__':
    try:
        Casper_Sensing()
    except rospy.ROSInterruptException:
        pass
