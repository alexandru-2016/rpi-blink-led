BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = "HIGH"
LOW = "LOW"

class pwm_cls:
   
   def __init__(self):
      pass

   def ChangeDutyCycle(self, a):
      print("GPIO PWM ChangeDutyCycle: ", a)

   def start(self, a):
      print("GPIO PWM Start: ", a)

   def stop(self):
      print("GPIO PWM Stop: ")


def setmode(a):
   print("GPIO Set mode: ", a)
def setup(a, b):
   print("GPIO Setup ", a, " ", b)
def output(a, b):
   print("GPIO Output ", a, " ", b)
def PWM(a, b):
   print("GPIO PWM ", a, " ", b)
   return pwm_cls()
def cleanup():
   print('GPIO Cleanup')
def setwarnings(flag):
   print("GPIO Set warnings ", flag)