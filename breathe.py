import time
import RPi.GPIO as GPIO
import pytweening

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        for repeat in range(1,3):
            for dc in range(100, 6, -2):
                ease = pytweening.easeOutQuad(dc / 100)
                #print("second: ", ease)
                p.ChangeDutyCycle(ease * 100)
                time.sleep(0.05)

            #time.sleep(1)

            for dc in range(38, 101, 2):
                ease = pytweening.easeInQuad(dc / 100)
                #print("first: ", ease)
                p.ChangeDutyCycle(ease * 100)
                time.sleep(0.05)

        # stay asleep a while longer when dark
        time.sleep(5)

except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
