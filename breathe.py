import time
import RPi.GPIO as GPIO
import pytweening

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            ease = pytweening.easeInQuad(dc / 100)
            p.ChangeDutyCycle(ease)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            ease = pytweening.easeOutQuad(dc / 100)
            p.ChangeDutyCycle(ease)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()