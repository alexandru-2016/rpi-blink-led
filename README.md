# rpi-blink-led

To run on RaspberryPi:

sudo apt-get install python-rpi.gpio python3-rpi.gpio
pip3 install PyTweening
pip3 install astral

delete the RPi folder, which is just for mocking the GPIO functionality outside of RaspberryPi environment

ln -s /home/pi/rpi-blink-led/breathe_led.service /lib/systemd/system/breathe_led.service