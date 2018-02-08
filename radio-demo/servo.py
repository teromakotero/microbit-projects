from microbit import *
import radio

pin0.set_analog_period(20) # Valmistellaan pin0 servoa varten (asetetaan PWM periodi 20 millisekuntiin)

radio.on() # Radio päälle
radio.config(channel = 50) # Valitse kanava 0-100 väliltä

while True: # Toistetaan ikuisesti

    viesti = radio.receive() # Etsitään ilmasta viesti

    if viesti != None: # Viesti löytyi!
        potentiometri = int(viesti) # Muutetaan viesti luvuksi
        dc = potentiometri * 0.1 + 0.02 # Muokataan potentiometrin arvo sopivaksi (2% ja 12% välille)
        pin0.write_analog(dc) # Liikutetaan servoa

    sleep(10) # Nukutaan 10 millisekuntia jottei toistolause mene liian nopeasti
