"""
LEVEL 10 - Parkovací senzor s ultrazvukovým čidlem HC-SR04

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 09 a přidáváme ultrazvukový senzor:
- PONECHÁVÁME: Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

- PŘIDÁVÁME: Ultrazvukový senzor HC-SR04 připojte:
  - VCC k 3V3 nebo 5V
  - GND k zemi (GND)  
  - TRIG k digitálnímu výstupu GP07 (spouštění měření)
  - ECHO k digitálnímu vstupu GP08 (příjem ozvěny)

V tomto příkladu se naučíte měřit vzdálenost pomocí ultrazvukového senzoru
a podle vzdálenosti měnit rychlost pípání jako u parkovacího senzoru v autě.
Čím blíže je překážka, tím rychleji senzor pípá.

NOVÉ KONCEPTY:
- Ultrazvukový senzor HC-SR04
- Měření vzdálenosti pomocí času ozvěny
- Knihovna adafruit_hcsr04 pro CircuitPython
- Mapování vzdálenosti na rychlost pípání
- Parkovací senzor - praktická aplikace
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import time         # funkce pro čekání a práci s časem
import simpleio     # modul pro jednoduché tóny
import adafruit_hcsr04  # knihovna pro ultrazvukový senzor HC-SR04

# vytvoření objektu pro ultrazvukový senzor
# TRIG na GP07, ECHO na GP08
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP7, echo_pin=board.GP8)

# konstanty pro parkovací senzor
MIN_VZDALENOST = 5    # minimální vzdálenost v cm (velmi blízko)
MAX_VZDALENOST = 100  # maximální vzdálenost v cm (daleko)
FREKVENCE_PIP = 800   # frekvence pípnutí
DELKA_PIP = 0.1       # délka jednoho pípnutí v sekundách

print("🚗 PARKOVACÍ SENZOR 🚗")
print(f"Rozsah měření: {MIN_VZDALENOST}cm - {MAX_VZDALENOST}cm")
print("Čím blíže překážka, tím rychlejší pípání")

# hlavní smyčka parkovacího senzoru
while True:
    try:
        # měření vzdálenosti v centimetrech
        vzdalenost = sonar.distance
        
        # omezení vzdálenosti na pracovní rozsah
        if vzdalenost < MIN_VZDALENOST:
            vzdalenost = MIN_VZDALENOST
        elif vzdalenost > MAX_VZDALENOST:
            vzdalenost = MAX_VZDALENOST
        
        # výpočet intervalu mezi pípnutími
        # blízko = krátký interval (rychlé pípání)
        # daleko = dlouhý interval (pomalé pípání)
        # mapujeme vzdálenost 5-100cm na interval 0.1-2.0s
        interval = 0.1 + (vzdalenost - MIN_VZDALENOST) * (2.0 - 0.1) / (MAX_VZDALENOST - MIN_VZDALENOST)
        
        # pípnutí
        simpleio.tone(board.GP6, FREKVENCE_PIP, DELKA_PIP)
        
        # výpis pro pochopení
        print(f"Vzdálenost: {vzdalenost:5.1f}cm, Interval: {interval:.2f}s")
        
        # čekání podle vypočítaného intervalu (mínus délka pípnutí)
        time.sleep(interval - DELKA_PIP)
        
    except RuntimeError:
        # chyba při měření - krátké čekání a pokus znovu
        print("Chyba měření - zkouším znovu...")
        time.sleep(0.1)
