#Libraries
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
#GPIO Pin variables
GPIO_TRIGGER = 18
GPIO_ECHO = 24
led = 4

#GPIO setups
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

p = GPIO.PWM(led,50)
p.start(0)

#function to measure distance using SR04
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            
            print ("Measured Distance = %.1f cm" % dist)
            
            if dist < 100: #Set LED to level of  ping within 1 Metre
                p.ChangeDutyCycle(100-dist)
            else: #Set LED to off if nothing to Ping
                p.ChangeDutyCycle(0)
            time.sleep(0.1)
            

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        p.stop()
        print("Measurement stopped by User")
        GPIO.cleanup()