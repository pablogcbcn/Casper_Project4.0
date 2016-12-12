#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from casper.msg import Sensing
from casper.msg import Stages

def callback_Stages(data):
    rospy.loginfo("Casper_Intelligence is talking")
    
def callback_Sensing(data):
    rospy.loginfo("Casper_Sensing is talking")

def Casper_Motion():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Casper_Motion', anonymous=True)

    #Casper_Motion subscription
    rospy.loginfo("Subscripting to topic Sensing_Results")
    rospy.Subscriber("Sensing_Results", Sensing, callback_Sensing)
    rospy.loginfo("Subscripting to topic Casper_Stages")
    rospy.Subscriber("Casper_Stages", Stages, callback_Stages)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        Casper_Motion()
    except rospy.ROSInterruptException:
	pass
