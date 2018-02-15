from microbit import *  # Tuodaan microbit kirjaston funktiot kayttoon.


# Jatkuvasti toistettavassa while -silmukassa valitaan napinpainallusten perusteella suoritettava ehtolause. elif = else if                
while True:
    if button_a.is_pressed():  # Jos a-nappainta pidetaan pohjassa, niin..
        display.scroll("Terve!")  # Naytossa juoksee teksti.
        
    elif button_b.was_pressed():  # Jos b-nappainta painettiin..
        display.show(Image.HEART)  # naytossa sydan 2 s ajan.
        sleep(2000)  # Odota 2 s eli 2000 millisekunttia
        display.clear()  # Tyhjenna naytto.
        # Kuva-animaatio, naytetaan kuvia 0.5 sekunnin valein. Yksittainen ledi sytytetetaan display.set_pixel(x,y,b)
        # b = kirkkaus valilla 0...9. Ledi vasen ylakulma koordinaatit (0,0), oikea-alakulma (4,4).
    
    elif (button_b.is_pressed() and button_a.was_pressed()):  # Jos b pidetaan pohjassa ja painetaan a:ta..
        display.show(Image.DIAMOND)  # Valmis kuva  microbitin kirjastosta. 
        sleep(500)
        display.show(Image.DIAMOND_SMALL)
        sleep(500)
        display.clear()
        display.set_pixel(2,2,9)  # Sytyta keskimmainen ledi, jonka koordinaatit (x,y)= (2,2) ja kirkkaus 9.
        sleep(500)
        
    else:  # Jos nappeja ei paineta, piirretaan hymio.
        display.show(Image.HAPPY)