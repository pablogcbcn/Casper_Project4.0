#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
from time import sleep
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention
from Libraries.RACOM.RACOM_TP import RACOM_TP
from Libraries.MPR121.mpr121 import *

RacomTP = None
sensing_msg = None
pub = None
rate = None

def set_I2C_register(address, register, value):
    global RacomTP
    data = [address, register, value]
    RacomTP.send(0x11, data)

def get_I2C_register(address, register):
    global RacomTP
    data = [address, register]
    RacomTP.send(0x10, data)
    while RacomTP.available() == 0:
        continue
    return RacomTP.read()

def get_I2C_Word(address, register):
    global RacomTP
    data = [address, register]
    RacomTP.send(0x12, data)
    while RacomTP.available() == 0:
        continue
    return RacomTP.read()

def initMpr121(): 
    set_I2C_register(0x5A, SOFT_RST, 0x63)
    sleep(0.001)
    set_I2C_register(0x5A, ELE_CFG, 0x00)
    set_I2C_register(0x5A, MHD_R, 0x01)
    set_I2C_register(0x5A, NHD_R, 0x01)
    set_I2C_register(0x5A, NCL_R, 0x5E)
    set_I2C_register(0x5A, FDL_R, 0x00)
    set_I2C_register(0x5A, MHD_F, 0x01)
    set_I2C_register(0x5A, NHD_F, 0x05)
    set_I2C_register(0x5A, NCL_F, 0x01)
    set_I2C_register(0x5A, FDL_F, 0x00)
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
    set_I2C_register(0x5A, DEBOUNCE, 0x00)
    set_I2C_register(0x5A, CONFIG1, 0x10)
    set_I2C_register(0x5A, FIL_CFG, 0x20)
    set_I2C_register(0x5A, ELE_CFG, 0x8F)
   
def Mpr121_Touch():
    global sensing_msg
    l = get_I2C_Word(0x5A,0x00)
    sensing_msg.mpr121L = l[0]
    sensing_msg.mpr121H = l[1]
    s = ""
    for i in range(4):
        s += str(1 & (l[1]>>(4-i)))
        s += "|"
    for i in range(8):
        s += str(1 & (l[0]>>(7-i)))
        s += "|"
    rospy.loginfo(s)

def readSensors():
    Mpr121_Touch()

def initSensors():
    initMpr121()
    rospy.loginfo("Mpr Initializated!")

def initTopics():
    global pub
    pub = rospy.Publisher('Sensing_Results', Sensing, queue_size=10)
    rospy.init_node('Casper_Sensing', anonymous=True)
    rospy.Rate(10) # 10hz


def Casper_Sensing():
    global pub
    while not rospy.is_shutdown():
        readSensors() 
        pub.publish(sensing_msg)

if __name__ == '__main__':
    global sensing_msg
    global RacomTP
    try:
        sensing_msg = Sensing()
        RacomTP = RACOM_TP("UART")
        initTopics()
        initSensors()
        Casper_Sensing()
    except rospy.ROSInterruptException:
        pass
