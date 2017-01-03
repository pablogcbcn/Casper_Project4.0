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

def initMpu6050():
    global timer = micros()
    set_I2C_register(0x68, 0x6B, 0x00)

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
    l = get_I2C_Word(0x5A,0x00)
    sensing_msg.mpr121L = l[0]
    sensing_msg.mpr121H = l[1]
    s = "Touch detection: "
    for i in range(4):
        s += str(1 & (l[1]>>(3-i)))
        s += "|"
    for i in range(8):
        s += str(1 & (l[0]>>(7-i)))
        s += "|"
    s=s.replace("1"," ")
    rospy.loginfo(s)

def Mpu6050_Accelerometer():
    l = get_I2C_Word(0x68, 0x3B)
    sensing_msg.mpuAcc_X = ((l[0] << 8) | l[1])
    l = get_I2C_Word(0x68, 0x3D)
    sensing_msg.mpuAcc_Y = ((l[0] << 8) | l[1])
    l = get_I2C_Word(0x68, 0x3F)
    sensing_msg.mpuAcc_Z = ((l[0] << 8) | l[1])
    s = "Accelerometer:   "
    s += str(sensing_msg.mpuAcc_X - initMpu6050.mpuAcc_X)
    s += "|"
    s += str(sensing_msg.mpuAcc_Y - initMpu6050.mpuAcc_Y)
    s += "|"
    s += str(sensing_msg.mpuAcc_Z - initMpu6050.mpuAcc_Z)
    rospy.loginfo(s)

def Mpu6050_Gyroscope():
    l = get_I2C_Word(0x68, 0x43)
    sensing_msg.mpuGyro_X = ((l[0] << 8) | l[1])
    l = get_I2C_Word(0x68, 0x45)
    sensing_msg.mpuGyro_Y = ((l[0] << 8) | l[1])
    l = get_I2C_Word(0x68, 0x47)
    sensing_msg.mpuGyro_Z = ((l[0] << 8) | l[1])
  
    dt = (double)(micros() - initMpu6050.timer) / 1000000; #This line does three things: 1) stops the timer, 2)converts the timer's output to seconds from microseconds, 3)casts the value as a double saved to "dt".
    initMpu6050.timer = micros(); #start the timer again so that we can calculate the next dt.

    #the next two lines calculate the orientation of the accelerometer relative to the earth and convert the output of atan2 from radians to degrees
    #We will use this data to correct any cumulative errors in the orientation that the gyroscope develops.
    roll = atan2(AcY, AcZ)*degconvert;
    pitch = atan2(-AcX, AcZ)*degconvert;

    #The gyroscope outputs angular velocities.  To convert these velocities from the raw data to deg/second, divide by 131.  
    #Notice, we're dividing by a double "131.0" instead of the int 131.
    gyroXrate = GyX/131.0;
    gyroYrate = GyY/131.0;

    #THE COMPLEMENTARY FILTER
    #This filter calculates the angle based MOSTLY on integrating the angular velocity to an angular displacement.
    #dt, recall, is the time between gathering data from the MPU6050.  We'll pretend that the 
    #angular velocity has remained constant over the time dt, and multiply angular velocity by 
    #time to get displacement.
    #The filter then adds a small correcting factor from the accelerometer ("roll" or "pitch"), so the gyroscope knows which way is down. 
    compAngleX = 0.99 * (compAngleX + gyroXrate * dt) + 0.01 * roll; # Calculate the angle using a Complimentary filter
    compAngleY = 0.99 * (compAngleY + gyroYrate * dt) + 0.01 * pitch; 

    s = "Gyroscope:       "
    s += str(compAngleX)
    s += "|"
    s += str(compAngleY)
    s += "|"
    rospy.loginfo(s)

def readSensors():
    global sensing_msg
    Mpr121_Touch()
    Mpu6050_Gyroscope()
    Mpu6050_Accelerometer()

def initSensors():
    initMpr121()
    initMpu6050()
    rospy.loginfo("Sensing Interface Initializated!")

def initTopics():
    global pub
    global rate
    pub = rospy.Publisher('Sensing_Results', Sensing, queue_size=10)
    rospy.init_node('Casper_Sensing', anonymous=True)
    rate = rospy.Rate(1) # 50hz


def Casper_Sensing():
    global pub
    while not rospy.is_shutdown():
        readSensors() 
        pub.publish(sensing_msg)
        rate.sleep()

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
