import sys

# search in current directory at the end
# local RPi module is for dev testing only
sys.path.append(sys.path.pop(0))

import signal
import time
from datetime import datetime
import pytz

import RPi.GPIO as GPIO
import pytweening
from astral import Astral

LED_PIN=18

dawn = datetime(2000, 1, 1, 10, 0, 0)
dusk = datetime(2000, 1, 1, 20, 0, 0)

def setup_location():
    global city
    
    city_name = 'Bucharest'
    a = Astral()
    a.solar_depression = 'civil'
    city = a[city_name]
    print('Solar data for %s/%s\n' % (city_name, city.region))

    timezone = city.timezone
    print('Timezone: %s' % timezone)


def setup_gpio():
    global p

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

    p = GPIO.PWM(LED_PIN, 50)  # channel=12 frequency=50Hz
    p.start(100)

def exit_gracefully(signum, frame):
    cleanup()
    exit()

def cleanup():
    if p:
        p.stop()
    
    GPIO.cleanup()
    print("Cleaned up GPIO")

def breathe(count, step_sleep, repeat_sleep):
    for repeat in range(count):
        for dc in range(1000, -1, -2):
            ease = pytweening.easeOutQuad(dc / 1000) * 100
            # print(ease)
            p.ChangeDutyCycle(ease)

            time.sleep(step_sleep)
        
        time.sleep(repeat_sleep)

        # print("ease out end")

        for dc in range(1, 1001, 2):
            ease = pytweening.easeInQuad(dc / 1000) * 100
            # print(ease)
            p.ChangeDutyCycle(ease)

            time.sleep(step_sleep)

        # print("ease in end")

        time.sleep(repeat_sleep)
    
    # make sure in the end we are at full on, no matter what breathe does
    p.ChangeDutyCycle(100)


def slow_breathe():
    breathe(3, 0.02, 1)


def normal_breathe():
    breathe(3, 0.005, 1)


def blink():
    breathe(3, 0.001, 0)

    # make sure in the end we are at full on, no matter what breathe does
    p.ChangeDutyCycle(100)


def update_sun_data(now):
    global dusk, dawn

    print("Computing sun data ...")
    sun = city.sun(date=now)

    print('Dawn:    %s' % str(sun['dawn']))
    # print('Sunrise: %s' % str(sun['sunrise']))
    # print('Noon:    %s' % str(sun['noon']))
    print('Dusk:    %s' % str(sun['dusk']))
    # print('Sunset:  %s' % str(sun['sunset']))

    dusk = sun['dusk']
    dawn = sun['dawn']


def check_day_sleep():
    global dusk, dawn

    now = datetime.now()
    # now = datetime(2019, 12, 11, 10, 0, 0)

    # From astral notes:
    # When creating a datetime object in a specific timezone 
    # do not use the tzinfo parameter to the datetime constructor. 
    # Instead please use the localize() method on the correct pytz timezone
    now = pytz.timezone(city.timezone).localize(now)

    # if day of now is not day of dawn, update sun data
    if now.date() != dawn.date():
        update_sun_data(now)

    if now < dusk and now > dawn:
        print("Good morning! Time is {}.".format(str(now)))
        print("Wake me up when the night shift starts.")

        p.ChangeDutyCycle(0)

        time_delta = dusk - now
        print("Set wake up timer to: {} ...".format(str(time_delta)))

        # in case ther is a problem with the delta computing, make sure sleep time is positive
        sleep_time = max(10, time_delta.total_seconds())
        time.sleep(sleep_time)
        
        print("Good evening!")


# main code starts here

setup_location()

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

setup_gpio()

while True:
    check_day_sleep()
    
    slow_breathe()
    time.sleep(10)

    normal_breathe()
    time.sleep(10)
    
    blink()
    time.sleep(5)
