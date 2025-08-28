"""
LEVEL 3 - Ovládání blikání tlačítkem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 2 - ponecháváme obě LED a přidáváme tlačítko:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) první LED veďte odpor 330Ω k zemi (GND)
- Zelenou LED připojte anodou (+) ke GP01  
- Z katody (-) druhé LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Tlačítko připojte jedním kontaktem ke GP02
- Druhý kontakt tlačítka připojte k zemi (GND)

V tomto příkladu se naučíte číst stav tlačítka a ovládat s ním blikání LED.
Tlačítko funguje jako přepínač - stisk zapne/vypne blikání.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import digitalio    # práce s digitálními vstupy a výstupy
import time         # funkce pro čekání a práci s časem

# vytvoření objektů pro LED
led1 = digitalio.DigitalInOut(board.GP0)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP1)
led2.direction = digitalio.Direction.OUTPUT

# vytvoření objektu pro tlačítko
button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # pull-up odpor pro stabilní čtení

# proměnné pro řízení stavu
blikani_zapnuto = False
posledni_stav = True  # tlačítko není stisknuto (pull-up = True)

print("Stiskněte tlačítko pro zapnutí/vypnutí blikání")

# hlavní smyčka
while True:
    # čtení aktuálního stavu tlačítka
    aktualni_stav = button.value
    
    # detekce stisku (změna z True na False)
    if posledni_stav == True and aktualni_stav == False:
        blikani_zapnuto = not blikani_zapnuto
        print(f"Blikání: {'ZAPNUTO' if blikani_zapnuto else 'VYPNUTO'}")
        time.sleep(0.2)  # krátká pauza proti "poskakování" tlačítka
    
    # uložení stavu pro příští porovnání
    posledni_stav = aktualni_stav
    
    # blikání LED pokud je zapnuté
    if blikani_zapnuto:
        led1.value = True
        led2.value = False
        time.sleep(0.5)
        
        led1.value = False
        led2.value = True
        time.sleep(0.5)
    else:
        # vypnuté LED
        led1.value = False
        led2.value = False
        time.sleep(0.01)
