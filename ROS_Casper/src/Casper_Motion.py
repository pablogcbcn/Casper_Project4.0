#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from casper.msg import Sensing
from casper.msg import Stages
from Libraries.RACOM.RACOM_TP import RACOM_TP


RacomTP = None
rate = None
st = "OFF"

def callback_Stages(data):
    rospy.loginfo("Casper_Intelligence is talking")
    
def callback_Sensing(data):
    return
    #rospy.loginfo("Casper_Sensing is talking")

def led_tgl():
    global RacomTP
    global st
    if st is "ON":
        if RacomTP.send(0x10, [0]) < 0:
            rospy.loginfo("RACOM sending error")
        st = "OFF"
    elif st is "OFF":
        if RacomTP.send(0x10, [1]) < 0:
            rospy.loginfo("RACOM sending error")
        st = "ON"

def Casper_Motion():
    global rate
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Casper_Motion', anonymous=True)
    rate = rospy.Rate(2)
    #Casper_Motion subscription
    rospy.loginfo("Subscripting to topic Sensing_Results")
    rospy.Subscriber("Sensing_Results", Sensing, callback_Sensing)
    rospy.loginfo("Subscripting to topic Casper_Stages")
    rospy.Subscriber("Casper_Stages", Stages, callback_Stages)
    
    while not rospy.is_shutdown():
        led_tgl()
        rate.sleep()


if __name__ == '__main__':
    global RacomTP
    try:
        RacomTP = RACOM_TP("I2C")
        Casper_Motion()
        
    except rospy.ROSInterruptException:
        pass
