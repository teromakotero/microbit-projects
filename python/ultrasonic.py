from microbit import *
import math

# Pinit
PIN_ECHO = pin0
PIN_TRIG = pin1

# Minimietäisyys joka näkyy näytöllä
MIN_DIST = 5.0
# Etäisyys joka mahtuu näytölle (näkyvä alue on siis MIN_DIST..MIN_DIST+DIST)
DIST = 30.0


# Toistofunktio (tässä tapahtuvat asiat tapahtuvat 50 kertaa sekunnissa jatkuvasti)
# (kts. tiedoston viimeiset rivit kutsua varten)
def loop():
    # Käynnistetään sensori
    trigger_echo()
    # Mitataan kaiun kesto
    duration = poll_duration()
    # Lasketaan matka
    distance = duration_to_distance(duration)
    # Esitetään matka LED-ruudulla
    #show_distance(distance)
    #display.set_pixel(0,0,9)
    display.scroll("D: " + str(distance))


# Käynnistä kaiku (mittaamista varten)
def trigger_echo():
    # Varmistetaan että TRIG on pois päältä
    PIN_TRIG.write_digital(True)
    sleep(1)
    # Käynnistetään TRIG
    PIN_TRIG.write_digital(False)
#    sleep(10)
    # Pistetään taas TRIG pois päältä
#    PIN_TRIG.write_digital(False)


# Mittaa kaiun pituus
def poll_duration():
    # Odotetaan että ECHO pin aktivoituu
    start_time = running_time()
    # While pyörii kunnes ECHO pin aktivoituu (tai menee liian pitkään)
    while not PIN_ECHO.read_digital():
        if running_time() - start_time > 5000:
            # Palautetaan oletusarvo koska ECHO pinillä meni liian pitkään
            return -1.0 * 2.0 * 29.1

    # ECHO pin on aktiivinen, mitataan kuinka kauan
    start_time = running_time()
    # While pyörii kunnes ECHO pin epäaktivoituu (tai menee liian pitkään)
    while PIN_ECHO.read_digital():
        if running_time() - start_time > 5000:
            # Palautetaan oletusarvo koska ECHO pinillä meni liian pitkään
            return 1000.0 * 2.0 * 29.1

    # Palautetaan kuinka pitkään meni (nykyhetki - aloitushetki)
    return running_time() - start_time


# Muuta kaiku-aika mitatuksi etäisyydeksi
def duration_to_distance(duration):
    # Lasketaan matka perustuen kaiun kestoon
    return (duration / 2.0) / 29.1


# Näytä etäisyys LED-näytöllä
def show_distance(distance):
    # Muutetaan distance ledien määräksi
    # Aluksi lasketaan matka MIN_DISTin jälkeen
    distance_from_min = distance - MIN_DIST
    # Muutetaan distance MINistä väliltä 0..DIST välille 0..5
    leds = min(5, max(0, 5.0 * distance_from_min / DIST))
    # Lasketaan kokonaisten ledien määrä, varmistetaan että niitä on maksimissaan 4
    led_count = min(4, int(leds))
    # Lasketaan viimeisen ylimääräisen ledin kirkkaus (ylijäämä kokonaisista)
    last_led_brightness = int(min(9, round(9 * (leds - led_count))))
    # Siivotaan ruutu
    display.clear()
    # Laitetaan led_count määrä ledejä päälle
    for i in range(led_count):
        set_pixel_column(i, i + 1, 9)
    # Laitetaan vielä viimeinen led päälle (mikäli sen kirkkaus on >0)
    if last_led_brightness > 0:
        set_pixel_column(led_count, led_count + 1, last_led_brightness)


# Aseta LED-kolumni "x" kirkkaudeksi "brightness" korkeudella "height"
# Eli "set_pixel_column(1, 2, 3)" tekee seuraavan:
# - Pistää ledejä päälle kolumnissa 1, eli toiset ledit vasemmalta (0 on vasen)
# - Pistää niitä 2 päälle, eli kaksi alinta (aloitetaan alhaalta)
# - Pistää ne ledit kirkkaudelle 3 (min kirkkaus on 0, max on 9)
def set_pixel_column(x, height, brightness):
    # Pistetään pixeleitä päälle pystysuunnassa heightin verran alhaalta ylös
    for i in range(5):
        # i on "kuinka mones led", joten pistetään päälle vain < height ledit
        if i < height:
            # Laitetaan päälle led kolumnissa x alkaen alhaalta (4)
            display.set_pixel(x, 4 - i, brightness)


# Toistetaan funktiota "loop" 50 kertaa sekunnissa
while True:
    loop()
    # "Nukutaan" 20 millisekuntia (0.02 sekuntia) jokaisen loopin välissä
    # (kun nukumme 0.02s, loopin taajuus on 50 Hz, sillä 1 / 0.02s = 50Hz)
    sleep(20)
