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

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

    p = GPIO.PWM(LED_PIN, 50)  # channel=12 frequency=50Hz
    p.start(100)

def exit_gracefully(signum, frame):
    cleanup()
    exit()

def cleanup():
    p.stop()
    GPIO.cleanup()
    print("Cleaned up GPIO")

def breathe(count):
    for repeat in range(count):
        for dc in range(100, 17, -2):
            ease = pytweening.easeOutQuad(dc / 100)
            #print("second: ", ease)
            p.ChangeDutyCycle(ease * 100)

            time.sleep(0.05)

        # print("Finished ease out")

        for dc in range(58, 101, 2):
            ease = pytweening.easeInQuad(dc / 100)
            #print("first: ", ease)
            p.ChangeDutyCycle(ease * 100)

            time.sleep(0.05)

        # print("Finished ease in")
        time.sleep(1)


def do_breath():
    breathe(6)
    p.ChangeDutyCycle(100)


def blink(count):
    for i in range(count):
        p.ChangeDutyCycle(30)
        time.sleep(0.3)
        p.ChangeDutyCycle(100)
        time.sleep(0.3)


def do_blink():
    blink(5)


setup_sun()
setup_gpio()


def update_sun_data(now):
    global dusk, dawn

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
        print("Computing sun data ...")
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


reset_sun_data()

while True:
    check_day_sleep()
    
    do_breath()
    time.sleep(5)
    do_blink()
    time.sleep(5)
