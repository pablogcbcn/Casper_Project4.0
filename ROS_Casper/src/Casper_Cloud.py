#!/usr/bin/env python
import rospy
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention

def callback(data):
    rospy.loginfo("I've received somthg")
    
def Casper_Cloud():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub = rospy.Publisher('Therapy_Intervention', Intervention, queue_size=10)
    rospy.init_node('Casper_Cloud', anonymous=True)

    #Casper_Cloud publishing
    rospy.loginfo("publishing to topic Therapy_Intervention")
    rate = rospy.Rate(10); #10Hz
    therapy_msg = Intervention();

    #Casper_Cloud subscription
    rospy.loginfo("Subscripting to topic Casper_Stages")
    rospy.Subscriber("Casper_Stages", Stages, callback)
    rospy.loginfo("Subscripting to topic Gaming_Results")
    rospy.Subscriber("Gaming_Results", Gaming, callback)
    rospy.loginfo("Subscripting to topic Sensing_Results")
    rospy.Subscriber("Sensing_Results", Sensing, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        Casper_Cloud()
    except rospy.ROSInterruptException:
	pass
