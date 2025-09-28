"""
LEVEL 14B - NeoPixel Matrix 4x4 - Interaktivní ovládání

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 14 a přidáváme tlačítko:
- PONECHÁVÁME: NeoPixel matrix 4x4:
  - VCC k 3V3 nebo 5V
  - GND k zemi (GND)
  - DIN k GP18

- PŘIDÁVÁME: Tlačítko pro přepínání vzorů:
  - Jeden pin tlačítka k GP02
  - Druhý pin k zemi (GND)
  - Interní pull-up odpor

V tomto příkladu budete moci tlačítkem přepínat mezi různými vzory
a efekty na NeoPixel matici. Každé stisknutí změní vzor nebo barvu.

NOVÉ KONCEPTY:
- Interaktivní ovládání LED efektů
- Stavový automat (state machine)
- Cyklické přepínání mezi módy
- Kombinace vstupu a výstupu
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import neopixel     # knihovna pro NeoPixel LED
import digitalio    # digitální vstupy a výstupy
import time         # funkce pro čekání a práci s časem

# konfigurace hardware
NEOPIXEL_PIN = board.GP18
BUTTON_PIN = board.GP02
NUM_PIXELS = 16
BRIGHTNESS = 0.2

# vytvoření objektů
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)
button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# barvy a vzory
COLORS = [
    (255, 0, 0),    # červená
    (0, 255, 0),    # zelená
    (0, 0, 255),    # modrá
    (255, 255, 0),  # žlutá
    (255, 0, 255),  # magenta
    (0, 255, 255),  # cyan
    (255, 255, 255) # bílá
]

PATTERNS = ["all", "corners", "cross", "frame", "diagonal", "checkerboard", "single", "rainbow"]

# stav programu
current_pattern = 0
current_color = 0
button_last_state = True
last_press_time = 0

def clear_matrix():
    """Vyčistí matrix"""
    pixels.fill((0, 0, 0))
    pixels.show()

def set_pixel(x, y, color):
    """Nastaví pixel na pozici x, y"""
    if 0 <= x < 4 and 0 <= y < 4:
        if y % 2 == 0:
            index = y * 4 + x
        else:
            index = y * 4 + (3 - x)
        pixels[index] = color

def show_pattern(pattern_name, color):
    """Zobrazí vzor s danou barvou"""
    clear_matrix()
    
    if pattern_name == "all":
        # Všechny LED stejnou barvou
        pixels.fill(color)
    
    elif pattern_name == "corners":
        # Pouze rohy
        set_pixel(0, 0, color)
        set_pixel(3, 0, color)
        set_pixel(0, 3, color)
        set_pixel(3, 3, color)
    
    elif pattern_name == "cross":
        # Kříž uprostřed
        for i in range(4):
            set_pixel(i, 1, color)
            set_pixel(i, 2, color)
            set_pixel(1, i, color)
            set_pixel(2, i, color)
    
    elif pattern_name == "frame":
        # Rámeček kolem
        for i in range(4):
            set_pixel(i, 0, color)
            set_pixel(i, 3, color)
            set_pixel(0, i, color)
            set_pixel(3, i, color)
    
    elif pattern_name == "diagonal":
        # Obě diagonály
        for i in range(4):
            set_pixel(i, i, color)
            set_pixel(i, 3-i, color)
    
    elif pattern_name == "checkerboard":
        # Šachovnice
        for x in range(4):
            for y in range(4):
                if (x + y) % 2 == 0:
                    set_pixel(x, y, color)
    
    elif pattern_name == "single":
        # Jedna LED postupně
        led_index = (int(time.monotonic() * 2)) % NUM_PIXELS
        pixels[led_index] = color
    
    elif pattern_name == "rainbow":
        # Duha (ignoruje color parametr)
        for i in range(NUM_PIXELS):
            hue = (i * 256 // NUM_PIXELS + int(time.monotonic() * 50)) % 256
            pixels[i] = wheel(hue)
    
    pixels.show()

def wheel(pos):
    """Generuje barvy pro duhový efekt"""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def handle_button():
    """Zpracuje stisk tlačítka s debouncing"""
    global current_pattern, current_color, button_last_state, last_press_time
    
    current_time = time.monotonic()
    button_current_state = button.value
    
    # Detekce sestupné hrany (stisk tlačítka)
    if button_last_state and not button_current_state:
        # Debouncing - ignoruj rychlé stisky
        if current_time - last_press_time > 0.3:
            # Přepni na další vzor
            current_pattern = (current_pattern + 1) % len(PATTERNS)
            
            # Při každém pátém vzoru změň barvu
            if current_pattern % 3 == 0:
                current_color = (current_color + 1) % len(COLORS)
            
            last_press_time = current_time
            
            pattern_name = PATTERNS[current_pattern]
            color_name = ["Červená", "Zelená", "Modrá", "Žlutá", "Magenta", "Cyan", "Bílá"][current_color]
            print(f"🎨 Vzor: {pattern_name.upper()}, Barva: {color_name}")
    
    button_last_state = button_current_state

print("🌈 INTERAKTIVNÍ NEOPIXEL MATRIX")
print("Stiskněte tlačítko pro změnu vzoru a barvy")
print("Vzory:", ", ".join(PATTERNS))

# počáteční vzor
pattern_name = PATTERNS[current_pattern]
print(f"🎨 Vzor: {pattern_name.upper()}, Barva: Červená")

while True:
    # Zpracuj tlačítko
    handle_button()
    
    # Zobraz aktuální vzor
    pattern_name = PATTERNS[current_pattern]
    color = COLORS[current_color]
    show_pattern(pattern_name, color)
    
    # Krátká pauza
    time.sleep(0.05)
