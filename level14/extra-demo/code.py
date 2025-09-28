"""
LEVEL 14 - NeoPixel Matrix 4x4 - Základní ovládání

ZAPOJENÍ OBVODU:
Pro tento level potřebujeme NeoPixel matrix 4x4:
- VCC k 3V3 nebo 5V (podle specifikace matice)
- GND k zemi (GND)
- DIN (Data Input) k GP18 (PWM výstup)

POZNÁMKA: NeoPixel matrix může potřebovat externí napájení při plném jasu.
Pro testování a nižší jas by mělo stačit napájení z Pico.

JAK FUNGUJE NEOPIXEL:
NeoPixel (WS2812) jsou adresovatelné RGB LED diody. Každá dioda obsahuje:
- Červený, zelený a modrý LED čip
- Integrovaný řadič (driver chip)
- Možnost řetězení více diod za sebou

Matrix 4x4 = 16 LED diod s indexy 0-15, uspořádané podle schématu výrobce.

NOVÉ KONCEPTY:
- Adresovatelné RGB LED (NeoPixel/WS2812)
- PWM signál pro řízení barev (24-bit RGB)
- Matrix indexování (2D -> 1D mapování)
- Barevné prostory (RGB, HSV)
- Animace a efekty
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import neopixel     # knihovna pro NeoPixel LED
import time         # funkce pro čekání a práci s časem

# konfigurace NeoPixel matrix 4x4
NEOPIXEL_PIN = board.GP18     # pin pro data signál
NUM_PIXELS = 16               # počet LED v matici (4x4)
BRIGHTNESS = 0.3              # jas (0.0 - 1.0, pozor na spotřebu!)

# vytvoření NeoPixel objektu
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

# základní barvy (RGB hodnoty 0-255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# seznam barev pro animace
COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]

def clear_matrix():
    """Vyčistí všechny LED (vypne je)"""
    pixels.fill(BLACK)
    pixels.show()

def set_pixel(x, y, color):
    """
    Nastaví barvu pixelu na pozici x, y (0-3)
    Mapuje 2D souřadnice na 1D index podle typického zapojení matrix
    """
    if 0 <= x < 4 and 0 <= y < 4:
        # Typické mapování pro 4x4 matrix (může se lišit podle výrobce)
        # Řádky se střídají: 0->3 zleva doprava, 4->7 zprava doleva, atd.
        if y % 2 == 0:  # sudé řádky (0, 2) - zleva doprava
            index = y * 4 + x
        else:  # liché řádky (1, 3) - zprava doleva
            index = y * 4 + (3 - x)
        
        pixels[index] = color

def show_pattern(pattern_name, color=RED):
    """Zobrazí předefinovaný vzor"""
    
    if pattern_name == "cross":
        # Kříž
        clear_matrix()
        for i in range(4):
            set_pixel(i, 1, color)  # horizontální čára
            set_pixel(1, i, color)  # vertikální čára
    
    elif pattern_name == "corners":
        # Rohy
        clear_matrix()
        set_pixel(0, 0, color)
        set_pixel(3, 0, color)
        set_pixel(0, 3, color)
        set_pixel(3, 3, color)
    
    elif pattern_name == "frame":
        # Rámeček
        clear_matrix()
        for i in range(4):
            set_pixel(i, 0, color)    # horní řada
            set_pixel(i, 3, color)    # dolní řada
            set_pixel(0, i, color)    # levý sloupec
            set_pixel(3, i, color)    # pravý sloupec
    
    elif pattern_name == "diagonal":
        # Diagonála
        clear_matrix()
        for i in range(4):
            set_pixel(i, i, color)
    
    elif pattern_name == "checkerboard":
        # Šachovnice
        clear_matrix()
        for x in range(4):
            for y in range(4):
                if (x + y) % 2 == 0:
                    set_pixel(x, y, color)
    
    pixels.show()

def rainbow_cycle():
    """Duuhový cyklus všemi LED"""
    for j in range(256):
        for i in range(NUM_PIXELS):
            # HSV do RGB převod pro duhový efekt
            pixel_hue = (i * 256 // NUM_PIXELS + j) % 256
            pixels[i] = wheel(pixel_hue)
        pixels.show()
        time.sleep(0.02)

def wheel(pos):
    """
    Generuje barvy pro duhový efekt (0-255)
    Vrací RGB tuple
    """
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def breathing_effect(color, duration=2.0):
    """Efekt dýchání - postupné rozsvícení a zhasnutí"""
    steps = 50
    for brightness in range(steps):
        # Postupné rozsvěcování
        factor = brightness / steps
        dimmed_color = (int(color[0] * factor), int(color[1] * factor), int(color[2] * factor))
        pixels.fill(dimmed_color)
        pixels.show()
        time.sleep(duration / (steps * 2))
    
    for brightness in range(steps, 0, -1):
        # Postupné zhasínání
        factor = brightness / steps
        dimmed_color = (int(color[0] * factor), int(color[1] * factor), int(color[2] * factor))
        pixels.fill(dimmed_color)
        pixels.show()
        time.sleep(duration / (steps * 2))

print("🌈 NEOPIXEL MATRIX 4x4")
print("Základní vzory a animace")
print("Stiskněte Ctrl+C pro ukončení")
print()

# hlavní smyčka s různými efekty
try:
    while True:
        print("📍 Zobrazuji kříž...")
        show_pattern("cross", RED)
        time.sleep(2)
        
        print("📐 Zobrazuji rohy...")
        show_pattern("corners", GREEN)
        time.sleep(2)
        
        print("🔲 Zobrazuji rámeček...")
        show_pattern("frame", BLUE)
        time.sleep(2)
        
        print("📏 Zobrazuji diagonálu...")
        show_pattern("diagonal", YELLOW)
        time.sleep(2)
        
        print("♟️ Zobrazuji šachovnici...")
        show_pattern("checkerboard", MAGENTA)
        time.sleep(2)
        
        print("🌬️ Efekt dýchání...")
        breathing_effect(CYAN)
        
        print("🌈 Duhový cyklus...")
        rainbow_cycle()
        
        print("⏸️ Pauza...")
        clear_matrix()
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🔴 Ukončuji program...")
    clear_matrix()
    print("Matrix vypnuta")
