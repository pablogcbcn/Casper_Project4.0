#!/usr/bin/env python
import rospy
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention

def callback(data):
    rospy.loginfo("I've received somthg")
    
def Casper_Display():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub = rospy.Publisher('Gaming_Results', Gaming, queue_size=10)
    rospy.init_node('Casper_Display', anonymous=True)

    #Casper_Display publishing
    rospy.loginfo("publishing to topic Gaming_Results")
    rate = rospy.Rate(10); #10Hz
    gaming_msg = Gaming();

    #Casper_Display subscription
    rospy.loginfo("Subscripting to topic Casper_Stages")
    rospy.Subscriber("Casper_Stages", Stages, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        Casper_Display()
    except rospy.ROSInterruptException:
	pass
