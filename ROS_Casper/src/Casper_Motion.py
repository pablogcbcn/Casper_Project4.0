#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from time import sleep
from casper.msg import Sensing
from casper.msg import Stages
from Libraries.RACOM.RACOM_TP import RACOM_TP


RacomTP = None

previous = None

def dynamixel_move(motor_id, position):
    global RacomTP
    data = [motor_id, position]
    self.RacomTP.send(0x10, data)

void Casper::Motion_goForward(){
  
    sleep(0.2)
    dynamixel_move(POS_L_P,70)
    sleep(0.050)
    dynamixel_move(INF_R_P,130)
    sleep(0.050)
    sleep(0.1)
    dynamixel_move(INF_L_P,90)
    sleep(0.050)
    dynamixel_move(POS_R_P,90)
    sleep(0.050)
    sleep(0.1)
    dynamixel_move(POS_L_A,130)
    sleep(0.050)
    dynamixel_move(INF_R_A,250)
    sleep(0.050)
    sleep(0.1)
    dynamixel_move(INF_L_A,180)
    sleep(0.050)
    dynamixel_move(POS_R_A,50)
    sleep(0.050)
    sleep(0.2)
    dynamixel_move(INF_L_P,40)
    sleep(0.050)
    dynamixel_move(POS_R_P,60)
    sleep(0.050)
    sleep(0.1)
    dynamixel_move(POS_L_P,120)
    sleep(0.050)
    dynamixel_move(INF_R_P,75)
    sleep(0.050)
    sleep(0.1)
    dynamixel_move(INF_L_A,110)
    sleep(0.050)
    dynamixel_move(POS_R_A,100)
    sleep(0.050)
    sleep(0.1)
    dynamixel_move(POS_L_A,180)
    sleep(0.050)
    dynamixel_move(INF_R_A,210)
    sleep(0.050)
     
     
def callback_Stages(data):
    rospy.loginfo("Casper_Intelligence is talking")
    
def callback_Sensing(data):
    global previous
    previous = data.mpr121

		
def Casper_Motion():
    global previous
    rospy.init_node('Casper_Motion', anonymous=True)
    #Casper_Motion subscription
    rospy.loginfo("Subscribing to topic Sensing_Results")
    rospy.Subscriber("Sensing_Results", Sensing, callback_Sensing)
    rospy.loginfo("Subscribing to topic Casper_Stages")
    rospy.Subscriber("Casper_Stages", Stages, callback_Stages)
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        if(previous > 0):
            Motion_goForward()
        rate.sleep()
    rospy.spin()


if __name__ == '__main__':
    global RacomTP
    try:
        RacomTP = RACOM_TP("/dev/ttyACM0")
        Casper_Motion()
        
    except rospy.ROSInterruptException:
        pass
