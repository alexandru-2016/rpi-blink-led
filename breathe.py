import signal
import time
import RPi.GPIO as GPIO

import pytweening
from astral import Astral

LED_PIN=18

def setup_sun():
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

while True:
    sun = city.sun()

    print('Dawn:    %s' % str(sun['dawn']))
    print('Sunrise: %s' % str(sun['sunrise']))
    print('Noon:    %s' % str(sun['noon']))
    print('Dusk:    %s' % str(sun['dusk']))
    print('Sunset:  %s' % str(sun['sunset']))

    do_breath()
    time.sleep(5)
    do_blink()
    time.sleep(5)
