#!/usr/bin/env python3
import ASUS.GPIO as GPIO
import time
import datetime

print('Starting script at: %s ' % datetime.datetime.now())

GPIO.setmode(GPIO.ASUS)
GPIO.setwarnings(False)

myservo=238
sleepTime=5

GPIO.setup(myservo,GPIO.OUT)
pwm = GPIO.PWM(myservo,5)
pwm.start(100)

time.sleep(sleepTime)
try:

    while True:
        actual_temp = 41000 #in case of problem with file reed, temp 41
        file = open('/sys/class/thermal/thermal_zone0/temp','r')
        actual_temp_string = file.read()
        file.close()
        try:
            actual_temp = int(actual_temp_string)
            actual_temp_in_degrees =int(round(actual_temp/1000))
            #print('Actual CPU temp: ',actual_temp_in_degrees)
        except ValueError as error:
            print('Conversion from string did not work',actual_temp_string)
        except ZeroDivisionError as err:
            print('Division by zero: ' ,actual_temp,err)

        if actual_temp_in_degrees > 55:
            pwm.ChangeDutyCycle(100)
        elif actual_temp_in_degrees > 50:
            pwm.ChangeDutyCycle(90)
        elif actual_temp_in_degrees > 45:
            pwm.ChangeDutyCycle(80)
        elif actual_temp_in_degrees > 40:
            pwm.ChangeDutyCycle(70)
        else:
            pwm.ChangeDutyCycle(60)

        #print('going to sleep')
        time.sleep(sleepTime)
except OSError:
    print('Can not open file')
except Exception as instance:
    print('Actual CPU temp: ',actual_temp_in_degrees)
    print(type(instance))
    print(instance.args)
    print(instance)

GPIO.cleanup()
print('Ending script at: %s' % datetime.datetime.now())
print('Script was terminated')
