from microbit import *
from math import *

pin1.set_analog_period(20) # 1000ms / 50Hz


def loop():
    potentiometer = pin0.read_analog() / 1024.0 # Read the potentiometer
    dutycycle = potentiometer * 0.1 + 0.02 # Map between 2% - 12%
    pin1.write_analog(dutycycle * 1024.0) # Move the servo
    rads = pi * 2 * potentiometer # Convert to radians

    # Draw
    x = cos(rads)
    y = sin(rads)
    display.clear()
    display.set_pixel(int(x * 2.5 + 2.4), int(y * 2.5 + 2.4), 9)


while True:
    loop()
    sleep(20)
