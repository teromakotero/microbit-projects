from microbit import *
import random

rock = Image("26952:"
             "69196:"
             "91019:"
             "69196:"
             "27962")
paper = Image("99999:"
              "97569:"
              "96579:"
              "96579:"
              "99999")
scissors = Image("00099:"
                 "79900:"
                 "93000:"
                 "79900:"
                 "00099")

loading0 = Image("00000:00000:09000:00000:00000")
loading1 = Image("00000:00000:09900:00000:00000")
loading2 = Image("00000:00000:09990:00000:00000")


def show_loading_bar():
    display.show(loading0)
    sleep(250)
    display.show(loading1)
    sleep(250)
    display.show(loading2)
    sleep(250)


def show_random_image():
    rand = random.randint(1, 3)
    if rand == 1:
        display.show(rock)
    if rand == 2:
        display.show(paper)
    if rand == 3:
        display.show(scissors)


while True:
    shaking = accelerometer.was_gesture("shake")
    flipped = accelerometer.was_gesture("face up")
    pressing = button_a.was_pressed() or button_b.was_pressed()
    if shaking or flipped or pressing:
        show_loading_bar()
        show_random_image()
