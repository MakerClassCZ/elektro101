"""
LEVEL 2 - Střídání dvou LED diod

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 1 - ponecháváme první LED a přidáváme druhou:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) první LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Druhou LED připojte anodou (+) ke GP01  
- Z katody (-) druhé LED veďte odpor 330Ω k zemi (GND)

V tomto příkladu se naučíte pracovat s více LED současně a koordinovat jejich chování.
Budeme střídat dvě LED - když jedna svítí, druhá je zhasnutá.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import digitalio    # práce s digitálními vstupy a výstupy
import time         # funkce pro čekání a práci s časem

# vytvoření objektu pro první LED (červená na GP00)
led1 = digitalio.DigitalInOut(board.GP0)
led1.direction = digitalio.Direction.OUTPUT

# vytvoření objektu pro druhou LED (zelená na GP01)
led2 = digitalio.DigitalInOut(board.GP1)
led2.direction = digitalio.Direction.OUTPUT

# nekonečná smyčka pro střídání LED
while True:
    # rozsvícení první, zhasnutí druhé LED
    led1.value = True
    led2.value = False
    time.sleep(0.5)
    
    # zhasnutí první, rozsvícení druhé LED
    led1.value = False
    led2.value = True
    time.sleep(0.5)
