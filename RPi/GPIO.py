BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = "HIGH"
LOW = "LOW"

def setmode(a):
   print("GPIO Set mode: ", a)
def setup(a, b):
   print("GPIO Setup ", a, " ", b)
def output(a, b):
   print("GPIO Output ", a, " ", b)
def cleanup():
   print('GPIO Cleanup')
def setwarnings(flag):
   print("GPIO Set warnings ", flag)