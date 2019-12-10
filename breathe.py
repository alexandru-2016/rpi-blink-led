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

def setup_sun():
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
        for dc in range(100, 5, -2):
            ease = pytweening.easeOutQuad(dc / 100)
            p.ChangeDutyCycle(ease * 100)

            time.sleep(step_sleep)

        # print("ease out end")

        for dc in range(34, 101, 2):
            ease = pytweening.easeInQuad(dc / 100)
            p.ChangeDutyCycle(ease * 100)

            time.sleep(step_sleep)

        # print("ease in end")

        time.sleep(repeat_sleep)


def do_breath():
    breathe(3, 0.05, 1)
    
    # make sure in the end we are at full on, no matter what breathe does
    p.ChangeDutyCycle(100)


def do_blink():
    breathe(3, 0.01, 0)

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


def reset_sun_data():
    global dusk, dawn

    dusk = None
    dawn = None


def check_day_sleep():
    global dusk, dawn

    now = datetime.now()
    # now = datetime(2019, 12, 11, 10, 0, 0)
    now = pytz.timezone(city.timezone).localize(now)

    if not dusk:
        update_sun_data(now)

    if now < dusk and now > dawn:
        print("Good morning! Time is {}.".format(str(now)))
        print("Wake me up when the night shift starts.")

        time_delta = dusk - now
        print("Set wake up timer to: {} ...".format(str(time_delta)))

        # in case ther is a problem with the delta computing
        sleep_time = max(10, time_delta.total_seconds())
        time.sleep(sleep_time)
        
        print("Good evening!")
        reset_sun_data()


# main code starts here

reset_sun_data()
setup_sun()

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

setup_gpio()

while True:
    check_day_sleep()
    
    do_breath()
    time.sleep(10)

    do_breath()
    time.sleep(10)
    
    do_blink()
    time.sleep(5)
