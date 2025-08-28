"""
LEVEL 1 - Blikání LED diody

ZAPOJENÍ OBVODU:
- Červenou LED připojte anodou (+, delší nožka) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)

V tomto jednoduchém příkladu se naučíte ovládat GPIO piny a blikat s LED.
Musíme inicializovat pin jako výstup a pak nastavovat jeho hodnoty.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import digitalio    # práce s digitálními vstupy a výstupy
import time         # funkce pro čekání a práci s časem

# vytvoření objektu pro LED připojenou ke GP00
led = digitalio.DigitalInOut(board.GP0)
# nastavení pinu jako výstup (budeme posílat signál ven)
led.direction = digitalio.Direction.OUTPUT

# nekonečná smyčka pro blikání
while True:
    # rozsvícení LED (True = vysoké napětí)
    led.value = True
    # čekání půl sekundy
    time.sleep(0.5)
    # zhasnutí LED (False = nízké napětí)
    led.value = False
    # čekání půl sekundy
    time.sleep(0.5)