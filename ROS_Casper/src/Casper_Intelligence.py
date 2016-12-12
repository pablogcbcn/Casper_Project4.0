#!/usr/bin/env python
import rospy
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention

def callback(data):
    rospy.loginfo("I've received somthg")
    
def Casper_Intelligence():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub = rospy.Publisher('Casper_Stages', Stages, queue_size=10)
    rospy.init_node('Casper_Intelligence', anonymous=True)

    #Casper_Intelligence publishing
    rospy.loginfo("publishing to topic Casper_Stages")
    rate = rospy.Rate(10); #10Hz
    stages_msg = Stages();

    #Casper_Intelligence subscription
    rospy.loginfo("Subscripting to topic Therapy_Intervention")
    rospy.Subscriber("Therapy_Intervention", Intervention, callback)
    rospy.loginfo("Subscripting to topic Gaming_Results")
    rospy.Subscriber("Gaming_Results", Gaming, callback)
    rospy.loginfo("Subscripting to topic Sensing_Results")
    rospy.Subscriber("Sensing_Results", Sensing, callback)

    while not rospy.is_shutdown():
       # rospy.loginfo(sensorList)
       pub.publish(stages_msg)
       rate.sleep()

if __name__ == '__main__':
    try:
        Casper_Intelligence()
    except rospy.ROSInterruptException:
	pass
