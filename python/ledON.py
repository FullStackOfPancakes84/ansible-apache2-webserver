#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)

for x in xrange(2):
    GPIO.output(16, GPIO.HIGH)
    time.sleep(.15)
    GPIO.output(16, GPIO.LOW)
    time.sleep(.15)

GPIO.output(16, GPIO.HIGH)
