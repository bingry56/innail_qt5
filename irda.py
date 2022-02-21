import RPi.GPIO as GPIO

import time



GPIO.setmode(GPIO.BCM)



pirPin = 21


GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

c = 0
while True:

    if GPIO.input(pirPin) ==  GPIO.LOW:

        print ("Motion detected!" + str(c))

    else:

        print ("No motion" +str(c))

    time.sleep(0.2)
    c = c+1