# Kytke nappi pietsokaiutin pinniin 1 ja gnd-porttiin. Nappin voita rakentaa kytkemalla johdon
# maadoitukseen, ja koskettamalla digiporttia 0.

from microbit import *

while True:
    if pin0.is_touched():
        pin1.write_digital(1)
    else: 
        pin1.write_digital(0)