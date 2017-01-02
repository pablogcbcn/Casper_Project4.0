#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from casper.msg import Sensing
from casper.msg import Stages
from Libraries.RACOM.RACOM_TP import RACOM_TP


RacomTP = None

previousL = 0
previousH = 0

def callback_Stages(data):
    rospy.loginfo("Casper_Intelligence is talking")
    
def callback_Sensing(data):
    global previousL
    global previousH
    previousL = data.mpr121L
    previousH = data.mpr121H
		
def Casper_Motion():
    rospy.init_node('Casper_Motion', anonymous=True)
    #Casper_Motion subscription
    rospy.loginfo("Subscribing to topic Sensing_Results")
    rospy.Subscriber("Sensing_Results", Sensing, callback_Sensing)
    rospy.loginfo("Subscribing to topic Casper_Stages")
    rospy.Subscriber("Casper_Stages", Stages, callback_Stages)
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        if(previousL!=0):
            RacomTP.send(0x10, [1])
        else:
            RacomTP.send(0x10, [0])
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    global RacomTP
    try:
        RacomTP = RACOM_TP("/dev/ttyACM0")
        Casper_Motion()
        
    except rospy.ROSInterruptException:
        pass
