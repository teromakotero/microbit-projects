from microbit import *


def etaisyys():
    pin1.write_digital(True)
    sleep(1)
    pin1.write_digital(False)

    aloitus_aika = running_time()
    lopetus_aika = running_time()

    display.set_pixel(0, 0, 9)
    while not pin0.read_digital():
        aloitus_aika = running_time()
    display.set_pixel(1, 0, 9)
    while pin0.read_digital():
        lopetus_aika = running_time()
    display.set_pixel(2, 0, 9)

    kulunut_aika = lopetus_aika - aloitus_aika
    etaisyys = (kulunut_aika * 34.3) / 2
    return etaisyys


while True:
    display.scroll("D: " + str(etaisyys()))
