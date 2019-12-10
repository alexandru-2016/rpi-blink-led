# rpi-blink-led

# RaspberryPi dependencies:
sudo apt-get install python-rpi.gpio python3-rpi.gpio
pip3 install PyTweening
pip3 install astral
pip3 install pytz

# install service
sudo ln -s /home/pi/rpi-blink-led/breathe_led.service /lib/systemd/system/breathe_led.service
sudo systemctl daemon-reload
sudo systemctl enable breathe_led.service