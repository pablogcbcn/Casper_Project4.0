#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
import math
from time import sleep
from datetime import datetime
from casper.msg import Sensing
from casper.msg import Stages
from casper.msg import Gaming
from casper.msg import Intervention
from Libraries.RACOM.RACOM_TP import RACOM_TP
from Libraries.MPR121.mpr121 import *
from Libraries.GPIO.GPIO import GPIO
from Libraries.I2C.I2C import I2C

RacomTP = None
sensing_msg = None
pub = None
rate = None
timer = None
ports = None
i2c = None

def initGPIO():
    global ports

    ports.set_GPIO_mode(13, ports.OUTPUT)
    ports.set_GPIO_mode(7, ports.INPUT)
    ports.set_GPIO(13, ports.HIGH)
    
def initMpu6050():
    global timer
    global dt
    global i2c

    i2c.set_I2C_register(0x68, 0x6B, 0x00)
    dt = datetime.now()
    timer = dt.microsecond
    #dt = rospy.get_rostime()
    #timer = dt.nsecs

def initMpr121():
    global i2c
 
    i2c.set_I2C_register(0x5A, SOFT_RST, 0x63)
    sleep(0.001)
    i2c.set_I2C_register(0x5A, ELE_CFG, 0x00)
    i2c.set_I2C_register(0x5A, MHD_R, 0x01)
    i2c.set_I2C_register(0x5A, NHD_R, 0x01)
    i2c.set_I2C_register(0x5A, NCL_R, 0x5E)
    i2c.set_I2C_register(0x5A, FDL_R, 0x00)
    i2c.set_I2C_register(0x5A, MHD_F, 0x01)
    i2c.set_I2C_register(0x5A, NHD_F, 0x05)
    i2c.set_I2C_register(0x5A, NCL_F, 0x01)
    i2c.set_I2C_register(0x5A, FDL_F, 0x00)
    i2c.set_I2C_register(0x5A, ELE0_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE0_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE1_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE1_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE2_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE2_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE3_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE3_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE4_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE4_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE5_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE5_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE6_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE6_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE7_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE7_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE8_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE8_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE9_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE9_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE10_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE10_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, ELE11_T, TOU_THRESH)
    i2c.set_I2C_register(0x5A, ELE11_R, REL_THRESH)
    i2c.set_I2C_register(0x5A, DEBOUNCE, 0x00)
    i2c.set_I2C_register(0x5A, CONFIG1, 0x10)
    i2c.set_I2C_register(0x5A, FIL_CFG, 0x20)
    i2c.set_I2C_register(0x5A, ELE_CFG, 0x8F)

def GPIO_Read(pin):
    global ports
    status = ports.get_GPIO(pin)
    rospy.loginfo(status[0])

def Mpr121_Touch():
    global i2c
    global sensing_msg

    l = i2c.get_I2C_Word(0x5A,0x00)
    mpr121L = l[0]
    mpr121H = l[1] & 0x1F
    mpr121 = l[0] | (mpr121H << 8)
    sensing_msg.mpr121 = mpr121
    #bro1 = 0x5555 & mpr121
    #bro2 = 0xAAAA & mpr121
    #vertical_swipe = ((((prev_bro2 >> 1) & bro1)%1) << 1 | (prev_bro1 & (bro2 >> 1)%1))
    #diagonal_swipe = ((((prev_bro2 << 1) & bro1)%1) << 1 | (prev_bro1 & (bro2 << 1)%1)) | ((((prev_bro2 >> 3) & bro1)%1) << 3 | (prev_bro1 & (bro2 >> 3)%1) << 2)
    


    #s = "Touch detection: "
    #for i in range(4):
    #    s += str(1 & (l[1]>>(3-i)))
    #     s += "|"
    #for i in range(8):
    #    s += str(1 & (l[0]>>(7-i)))
    #    s += "|"
    #s=s.replace("1"," ")
    #rospy.loginfo(s)

def Mpu6050_Accelerometer():
    global i2c
    l = i2c.get_I2C_Word(0x68, 0x3B)
    sensing_msg.mpuAcc_X = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x3D)
    sensing_msg.mpuAcc_Y = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x3F)
    sensing_msg.mpuAcc_Z = ((l[0] << 8) | l[1])
    s = "Accelerometer:   "
    s += str(sensing_msg.mpuAcc_X)
    s += "|"
    s += str(sensing_msg.mpuAcc_Y)
    s += "|"
    s += str(sensing_msg.mpuAcc_Z)
    rospy.loginfo(s)

def Mpu6050_Gyroscope():
    global timer
    global sensing_msg
    global dt
    global i2c


    l = i2c.get_I2C_Word(0x68, 0x43)
    GyX = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x45)
    GyY = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x47)
    Gy_Z = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x3B)
    AcX = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x3D)
    AcY = ((l[0] << 8) | l[1])
    l = i2c.get_I2C_Word(0x68, 0x3F)
    AcZ = ((l[0] << 8) | l[1])
    if AcX > 32768:
        AcX = (65536 - AcX)* (-1)
    if AcY > 32768:
        AcY = (65536 - AcY)* (-1)
    if AcZ > 32768:
        AcZ = (65536 - AcZ)* (-1)
    if GyX > 32768:
        GyX = (65536 - GyX)* (-1)
    if GyY > 32768:
        GyY = (65536 - GyY)* (-1)
    dt = datetime.now()
    if dt.microsecond > timer:
        deltat = (dt.microsecond - timer)/1000000.0 #This line does three things: 1) stops the timer, 2)converts the timer's output to seconds from microseconds, 3)casts the value as a double saved to "dt".
        
        #the next two lines calculate the orientation of the accelerometer relative to the earth and convert the output of atan2 from radians to degrees
        #We will use this data to correct any cumulative errors in the orientation that the gyroscope develops.
        roll = math.atan2(AcY, AcZ)*57.2957786
        pitch = math.atan2(-AcX, AcZ)*57.2957786
        
        #The gyroscope outputs angular velocities.  To convert these velocities from the raw data to deg/second, divide by 131.  
        #Notice, we're dividing by a double "131.0" instead of the int 131.
        gyroXrate = GyX/131.0
        gyroYrate = GyY/131.0

        #THE COMPLEMENTARY FILTER
        #This filter calculates the angle based MOSTLY on integrating the angular velocity to an angular displacement.
        #dt, recall, is the time between gathering data from the MPU6050.  We'll pretend that the 
        #angular velocity has remained constant over the time dt, and multiply angular velocity by 
        #time to get displacement.
        #The filter then adds a small correcting factor from the accelerometer ("roll" or "pitch"), so the gyroscope knows which way is down. 
        sensing_msg.mpuGyro_X = 0.99 * (sensing_msg.mpuGyro_X + gyroXrate * deltat) + 0.01 * roll # Calculate the angle using a Complimentary filter
        sensing_msg.mpuGyro_Y = 0.99 * (sensing_msg.mpuGyro_Y + gyroYrate * deltat) + 0.01 * pitch
    
    dt = datetime.now()
    timer = dt.microsecond
    s = "Gyroscope:       "
    s += str(sensing_msg.mpuGyro_X)
    s += "|"
    s += str(sensing_msg.mpuGyro_Y)
    s += "|"
    rospy.loginfo(s)

def readSensors():
    global sensing_msg
    #Mpr121_Touch()
    #Mpu6050_Gyroscope()
   # Mpu6050_Accelerometer()
    GPIO_Read(7)

def initSensors():
    #initMpr121()
    #initMpu6050()
    initGPIO()
    rospy.loginfo("Sensing Interface Initializated!")

def initTopics():
    global pub
    global rate
    pub = rospy.Publisher('Sensing_Results', Sensing, queue_size=10)
    rospy.init_node('Casper_Sensing', anonymous=True)

    rate = rospy.Rate(1000) # 50hz


def Casper_Sensing():
    global pub
    global timer
    global dt

    while not rospy.is_shutdown():
        readSensors() 
        pub.publish(sensing_msg)
        rate.sleep()

if __name__ == '__main__':
    global sensing_msg
    global RacomTP
    global ports
    try:
        ports = GPIO()
        i2c = I2C()
        sensing_msg = Sensing()
        RacomTP = RACOM_TP("UART")
        initTopics()
        initSensors()
        Casper_Sensing()
    except rospy.ROSInterruptException:
        pass
