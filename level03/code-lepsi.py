"""
LEVEL 3 - Ovládání blikání tlačítkem (LEPŠÍ ŘEŠENÍ)

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 2 - ponecháváme obě LED a přidáváme tlačítko:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) první LED veďte odpor 330Ω k zemi (GND)
- Zelenou LED připojte anodou (+) ke GP01  
- Z katody (-) druhé LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Tlačítko připojte jedním kontaktem ke GP02
- Druhý kontakt tlačítka připojte k zemi (GND)

Toto je vylepšená verze, která řeší problém s blokováním při sleep().
Místo dlouhých čekání používáme neblokující časování a specializovanou
knihovnu keypad pro profesionální práci s tlačítky.

VYLEPŠENÍ:
- Tlačítko reaguje okamžitě, i během blikání
- Automatické debouncing pomocí keypad knihovny
- Event-driven programování s frontou událostí
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import digitalio    # práce s digitálními vstupy a výstupy
import time         # funkce pro čekání a práci s časem
import keypad       # pokročilá práce s tlačítky a událostmi

# vytvoření objektů pro LED
led1 = digitalio.DigitalInOut(board.GP0)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP1)
led2.direction = digitalio.Direction.OUTPUT

# vytvoření keypad objektu pro tlačítko s automatickým debouncing
keys = keypad.Keys((board.GP2,), value_when_pressed=False, pull=True)

# proměnné pro řízení stavu
blikani_zapnuto = False
led_stav = False  # True = led1 svítí, False = led2 svítí
posledni_cas = time.monotonic()

# konstanta pro rychlost blikání
RYCHLOST_BLIKANI = 0.5

print("Stiskněte tlačítko pro zapnutí/vypnutí blikání")

# hlavní smyčka s event-driven přístupem
while True:
    # kontrola událostí tlačítka
    event = keys.events.get()
    
    if event and event.pressed:
        # přepnutí stavu blikání
        blikani_zapnuto = not blikani_zapnuto
        print(f"Blikání: {'ZAPNUTO' if blikani_zapnuto else 'VYPNUTO'}")
        
        # vypnutí LED při zastavení blikání
        if not blikani_zapnuto:
            led1.value = False
            led2.value = False

    # neblokující blikání pomocí časování
    if blikani_zapnuto:
        aktualni_cas = time.monotonic()
        
        if aktualni_cas - posledni_cas >= RYCHLOST_BLIKANI:
            # přepnutí LED
            led_stav = not led_stav
            led1.value = led_stav
            led2.value = not led_stav
            
            posledni_cas = aktualni_cas
    
    # krátká pauza pro stabilitu
    time.sleep(0.01)
