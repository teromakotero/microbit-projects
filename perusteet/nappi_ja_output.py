# Napin b-painallus kaynnistaa pin0:aan kytketyn pietso-kaiuttimen tai led-lampun.
# Ulkoisen laitteen kytkenta: GND ja pin0. Jos kaytat ledia, niin pidempi +-napa pin0:aan.

from microbit import *  # Tuodaan python kirjasto kayttoon.

# Toistetteva silmukka
while True:
    if button_b.is_pressed():  # Jos nappia painetaan, jannite nostetaan ylos 3.3V:iin.
        pin0.write_digital(1)
    else:  # Muussa tapauksessa laite sammutetaan.
        pin0.write_digital(0)