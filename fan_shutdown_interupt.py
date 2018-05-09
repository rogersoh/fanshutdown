#!/usr/bin/env python3
# Author: Andreas Spiess
import os #shutdown command
import time #for timer example sleep
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

fanPin = 17 # The pin ID, edit here to change it
batterySensPin = 18
maxTMP = 20 # The maximum temperature in Celsius after which we trigger the fan
GPIO.setup(batterySensPin, GPIO.IN, GPIO.PUD_UP)

def Shutdown(channel):
  sleep(2)
  if GPIO.input(batterySensPin)==0:
       os.system("sudo shutdown -h")
       GPIO.output(fanPin, GPIO.LOW)
       sleep(5)
       GPIO.output(fanPin, GPIO.HIGH)
       sleep(100)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fanPin, GPIO.OUT)
   # GPIO.setup(batterySensPin, GPIO.IN, GPIO.PUD_UP)
    GPIO.setwarnings(False)
    #fanOFF()
    GPIO.output(fanPin, GPIO.LOW)
    return()

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    #print("temp is {0}".format(temp)) #Uncomment here for testing
    return temp

def fanON():
    setPin(True)
    return()

def fanOFF():
    setPin(False)
    return()

def handleFan():
    CPU_temp = float(getCPUtemperature())
    if CPU_temp>maxTMP:
        #fanON()
        GPIO.output(fanPin, GPIO.HIGH)
        #print("fan on")
    if CPU_temp<maxTMP-5:
        #fanOFF()
       GPIO.output(fanPin, GPIO.LOW)
        #print("fan off")
    return()

# USE INTERUPT TO Shutdown
GPIO.add_event_detect(batterySensPin, GPIO.FALLING, Shutdown, 600)

def setPin(mode): # A little redundant function but useful if you want to add logging
    #GPIO.output(fanPin, mode)
    return()

try:
    setup() 
    while True:
        handleFan()
        #handleBattery()
        sleep(5) # Read the temperature every 5 sec, increase or decrease this limit if you want

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
    fanOFF()
    GPIO.cleanup() # resets all GPIO ports used by this program
