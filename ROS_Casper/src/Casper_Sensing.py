#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
import time
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention
from Libraries.RACOM import RACOM_TP
from Libraries.MPR121 import mpr121

RacomTP = None
sensing_msg = None
pub = None
rate = None

def set_I2C_register(address, register, value):

    data = [address, register, value]
    send(0x11, 3, data)

def get_I2C_register(address, register):

    data = [address, register]
    send(0x10, 2, data)
    while RacomTP.available() == 0:
	pass
    return RacomTP.read()

def initMpr121(): 

    set_I2C_register(0x5A, ELE_CFG, 0x00)
    set_I2C_register(0x5A, MHD_R, 0x01)
    set_I2C_register(0x5A, NHD_R, 0x01)
    set_I2C_register(0x5A, NCL_R, 0x00)
    set_I2C_register(0x5A, FDL_R, 0x00)
    set_I2C_register(0x5A, MHD_F, 0x01)
    set_I2C_register(0x5A, NHD_F, 0x01)
    set_I2C_register(0x5A, NCL_F, 0xFF)
    set_I2C_register(0x5A, FDL_F, 0x02)
    set_I2C_register(0x5A, ELE0_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE0_R, REL_THRESH)
    set_I2C_register(0x5A, ELE1_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE1_R, REL_THRESH)
    set_I2C_register(0x5A, ELE2_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE2_R, REL_THRESH)
    set_I2C_register(0x5A, ELE3_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE3_R, REL_THRESH)
    set_I2C_register(0x5A, ELE4_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE4_R, REL_THRESH)
    set_I2C_register(0x5A, ELE5_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE5_R, REL_THRESH)
    set_I2C_register(0x5A, ELE6_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE6_R, REL_THRESH)
    set_I2C_register(0x5A, ELE7_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE7_R, REL_THRESH)
    set_I2C_register(0x5A, ELE8_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE8_R, REL_THRESH)
    set_I2C_register(0x5A, ELE9_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE9_R, REL_THRESH)
    set_I2C_register(0x5A, ELE10_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE10_R, REL_THRESH)
    set_I2C_register(0x5A, ELE11_T, TOU_THRESH)
    set_I2C_register(0x5A, ELE11_R, REL_THRESH)
    set_I2C_register(0x5A, FIL_CFG, 0x04)
    set_I2C_register(0x5A, ELE_CFG, 0x0C) 
    set_I2C_register(0x5A, ELE_CFG, 0x0C)
   
def Mpr121_Touch():
    
    sensing_msg.mpr121L = get_I2C_register(0x5A, 0x00)
    sensing_msg.mpr121L = get_I2C_register(0x5A, 0x01)
    rospy.loginfo("Values read from arduino:\n")
    rospy.loginfo(sensing_msg.mpr121L)
    rospy.loginfo(sensing_msg.mpr121H)

def readSensors():
    
    Mpr121_Touch()

def initSensors():

    initMpr121()
    rospy.loginfo("MprInitializated!")

def initTopics():

    pub = rospy.Publisher('Sensing_Results', Sensing, queue_size=10)
    rospy.init_node('Casper_Sensing', anonymous=True)
    rospy.loginfo("publishing to topic Sensing_Results")
    #rate = rospy.Rate(10) # 10hz

def Casper_Sensing():

    while not rospy.is_shutdown():
        readSensors() 
        pub.publish(sensing_msg)
        rospy.loginfo("Some publish madafaka\n")
        sleep(2)

if __name__ == '__main__':
    try:
        sensing_msg = Sensing()
        RacomTP = RACOM_TP("UART")
	initSensors()
	initTopics()
        Casper_Sensing()
    except rospy.ROSInterruptException:
        pass
