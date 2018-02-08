from microbit import *
import radio

radio.on() # Radio päälle
radio.config(channel = 50) # Valitse kanava 0-100 väliltä

potentiometri = 0 # Alustetaan potentiometri 0:n

while True:
    potentiometri_uusi = pin0.read_analog() # Luetaan potentiometrin arvo

    if potentiometri != potentiometri_uusi: # Uusi lukema on eri, potentiometriä on liikutettu -> Lähetetään viesti!
        radio.send(str(potentiometri)) # Lähetetään potentiometrin arvo tekstinä

    potentiometri = potentiometri_uusi # Päivitetään potentiometrin arvo seuraavaa kertaa varten

    sleep(30) # Nukutaan 30 millisekuntia jottei toistolause mene liian nopeasti
