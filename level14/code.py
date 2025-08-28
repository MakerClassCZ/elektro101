"""
LEVEL 14 - NeoPixel Matrix 4x4 - Základní postupné rozsvěcování

ZAPOJENÍ OBVODU:
NeoPixel matrix 4x4 připojte:
- VCC k 3V3 nebo 5V (podle specifikace matice)
- GND k zemi (GND)
- DIN (Data Input) k GP18

POZNÁMKA: NeoPixel matrix může potřebovat externí napájení při plném jasu.
Pro testování a nižší jas by mělo stačit napájení z Pico.

JAK FUNGUJE NEOPIXEL:
NeoPixel (WS2812) jsou adresovatelné RGB LED diody uspořádané v matici.
Každá LED má svůj index (0-15) a můžeme ji ovládat nezávisle.
Matrix 4x4 = 16 LED diod, které rozsvěcujeme postupně jedna po druhé.

V tomto příkladu postupně rozsvítíme všechny LED:
1. Nejprve červeně (LED 0-15)
2. Pak zeleně (LED 0-15)  
3. Pak modře (LED 0-15)
4. A opakujeme od začátku

NOVÉ KONCEPTY:
- Adresovatelné RGB LED (NeoPixel/WS2812)
- Postupné ovládání jednotlivých LED
- RGB barvy (255, 0, 0) = červená
- Cyklické opakování sekvence
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import neopixel     # knihovna pro NeoPixel LED
import time         # funkce pro čekání a práci s časem

# konfigurace NeoPixel matrix 4x4
NEOPIXEL_PIN = board.GP18     # pin pro data signál
NUM_PIXELS = 16               # počet LED v matici (4x4 = 16)
BRIGHTNESS = 0.3              # jas (0.0 - 1.0, pozor na spotřebu!)

# vytvoření NeoPixel objektu
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

# definice barev (R, G, B) - hodnoty 0-255
RED = (255, 0, 0)      # červená
GREEN = (0, 255, 0)    # zelená
BLUE = (0, 0, 255)     # modrá
BLACK = (0, 0, 0)      # černá (vypnuto)

# seznam barev pro cyklování
COLORS = [RED, GREEN, BLUE]
COLOR_NAMES = ["Červená", "Zelená", "Modrá"]

def clear_all():
    """Vypne všechny LED"""
    pixels.fill(BLACK)
    pixels.show()

def light_pixel(index, color):
    """Rozsvítí jednu LED na daném indexu"""
    pixels[index] = color
    pixels.show()

print("🌈 NEOPIXEL MATRIX 4x4 - Postupné rozsvěcování")
print("LED se rozsvěcují postupně jedna po druhé")
print("Pořadí barev: Červená → Zelená → Modrá → opakování")


# hlavní smyčka
while True:
    # Projdi všechny barvy
    for color_index, color in enumerate(COLORS):
        color_name = COLOR_NAMES[color_index]
        print(f"🎨 {color_name} - rozsvěcuji LED 0-15...")
        
        # Nejprve vypni všechny LED
        clear_all()
        
        # Postupně rozsvěcuj všechny LED aktuální barvou
        for pixel_index in range(NUM_PIXELS):
            light_pixel(pixel_index, color)
            print(f"  LED {pixel_index:2d}: ■")
            time.sleep(0.2)  # pauza mezi LED (200ms)
        
        # Krátká pauza na konci barvy
        print(f"  ✅ Všech 16 LED {color_name.lower()}")
        time.sleep(1)
    
    print("🔄 Opakuji od začátku...\n")
