"""
LEVEL 14C - NeoPixel Matrix 4x4 - Ovládání enkodérem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 14 a přidáváme rotační enkodér:
- PONECHÁVÁME: NeoPixel matrix 4x4:
  - VCC k 3V3 nebo 5V
  - GND k zemi (GND)
  - DIN k GP18

- PŘIDÁVÁME: Rotační enkodér pro plynulé ovládání:
  - GND k zemi (GND)
  - + k ADC_VREF (napájení enkodéru)
  - DT k GP03 (A kanál)
  - CLK k GP04 (B kanál)
  - SW k GP02 (tlačítko enkodéru)

V tomto příkladu budete moci enkodérem měnit jas a barvy,
tlačítkem enkodéru přepínat mezi módy ovládání.

NOVÉ KONCEPTY:
- Rotační enkodér pro analogové ovládání
- Dynamická změna jasu
- HSV barevný prostor (Hue, Saturation, Value)
- Módy ovládání (jas, barva, vzor)
- Kombinace digitálního a analogového vstupu
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import neopixel     # knihovna pro NeoPixel LED
import rotaryio     # rotační enkodér
import digitalio    # digitální vstupy a výstupy
import time         # funkce pro čekání a práci s časem
import math         # matematické funkce

# konfigurace hardware
NEOPIXEL_PIN = board.GP18
ENCODER_A = board.GP4
ENCODER_B = board.GP3
ENCODER_SW = board.GP02
NUM_PIXELS = 16

# vytvoření objektů
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.3, auto_write=False)
encoder = rotaryio.IncrementalEncoder(ENCODER_A, ENCODER_B)
encoder_button = digitalio.DigitalInOut(ENCODER_SW)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP

# stavy ovládání
MODES = ["brightness", "hue", "pattern"]
current_mode = 0
last_encoder_position = 0
button_last_state = True
last_button_time = 0

# parametry
brightness = 0.3    # jas (0.0 - 1.0)
hue = 0            # odstín (0 - 360)
pattern_index = 0  # index vzoru

# vzory
PATTERNS = [
    "solid",        # jednolitá barva
    "gradient",     # gradient
    "pulse",        # pulzování
    "rotate",       # rotace
    "sparkle",      # jiskření
    "wave"          # vlna
]

def clear_matrix():
    """Vyčistí matrix"""
    pixels.fill((0, 0, 0))
    pixels.show()

def hsv_to_rgb(h, s, v):
    """
    Převede HSV na RGB
    h: hue (0-360)
    s: saturation (0-1)
    v: value/brightness (0-1)
    """
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def set_pixel(x, y, color):
    """Nastaví pixel na pozici x, y"""
    if 0 <= x < 4 and 0 <= y < 4:
        if y % 2 == 0:
            index = y * 4 + x
        else:
            index = y * 4 + (3 - x)
        pixels[index] = color

def show_pattern():
    """Zobrazí aktuální vzor"""
    pattern = PATTERNS[pattern_index]
    current_time = time.monotonic()
    
    if pattern == "solid":
        # Jednolitá barva
        color = hsv_to_rgb(hue, 1.0, 1.0)
        pixels.fill(color)
    
    elif pattern == "gradient":
        # Horizontální gradient
        for x in range(4):
            for y in range(4):
                h = (hue + x * 30) % 360
                color = hsv_to_rgb(h, 1.0, 1.0)
                set_pixel(x, y, color)
    
    elif pattern == "pulse":
        # Pulzování celé matice
        pulse = (math.sin(current_time * 3) + 1) / 2  # 0-1
        color = hsv_to_rgb(hue, 1.0, pulse)
        pixels.fill(color)
    
    elif pattern == "rotate":
        # Rotující bod
        angle = current_time * 2  # radiány
        center_x, center_y = 1.5, 1.5
        x = int(center_x + 1.2 * math.cos(angle))
        y = int(center_y + 1.2 * math.sin(angle))
        
        clear_matrix()
        color = hsv_to_rgb(hue, 1.0, 1.0)
        if 0 <= x < 4 and 0 <= y < 4:
            set_pixel(x, y, color)
            # Přidej slabší stopu
            prev_x = int(center_x + 1.2 * math.cos(angle - 0.5))
            prev_y = int(center_y + 1.2 * math.sin(angle - 0.5))
            if 0 <= prev_x < 4 and 0 <= prev_y < 4:
                dim_color = hsv_to_rgb(hue, 1.0, 0.3)
                set_pixel(prev_x, prev_y, dim_color)
    
    elif pattern == "sparkle":
        # Náhodné jiskření
        import random
        clear_matrix()
        for _ in range(random.randint(1, 4)):
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            h = (hue + random.randint(-60, 60)) % 360
            color = hsv_to_rgb(h, 1.0, random.uniform(0.3, 1.0))
            set_pixel(x, y, color)
    
    elif pattern == "wave":
        # Vlnový efekt
        for x in range(4):
            for y in range(4):
                wave = math.sin(current_time * 2 + x * 0.5 + y * 0.5)
                intensity = (wave + 1) / 2  # 0-1
                color = hsv_to_rgb(hue, 1.0, intensity)
                set_pixel(x, y, color)
    
    # Aplikuj globální jas
    pixels.brightness = brightness
    pixels.show()

def handle_encoder():
    """Zpracuje rotaci enkodéru"""
    global last_encoder_position, brightness, hue, pattern_index
    
    current_position = encoder.position
    delta = current_position - last_encoder_position
    
    if delta != 0:
        mode = MODES[current_mode]
        
        if mode == "brightness":
            brightness += delta * 0.05
            brightness = max(0.05, min(1.0, brightness))
            print(f"💡 Jas: {brightness:.2f}")
        
        elif mode == "hue":
            hue += delta * 5
            hue = hue % 360
            print(f"🎨 Odstín: {hue}°")
        
        elif mode == "pattern":
            pattern_index += delta
            pattern_index = pattern_index % len(PATTERNS)
            pattern_name = PATTERNS[pattern_index]
            print(f"🔄 Vzor: {pattern_name.upper()}")
        
        last_encoder_position = current_position

def handle_button():
    """Zpracuje tlačítko enkodéru"""
    global current_mode, button_last_state, last_button_time
    
    current_time = time.monotonic()
    button_current_state = encoder_button.value
    
    if button_last_state and not button_current_state:
        if current_time - last_button_time > 0.3:
            current_mode = (current_mode + 1) % len(MODES)
            mode_name = MODES[current_mode]
            mode_names = {"brightness": "Jas", "hue": "Barva", "pattern": "Vzor"}
            print(f"⚙️ Mód: {mode_names[mode_name]}")
            last_button_time = current_time
    
    button_last_state = button_current_state

print("🌈 NEOPIXEL S ENKODÉREM")
print("Rotací enkodéru měníte aktuální parametr")
print("Tlačítkem enkodéru přepínáte módy:")
print("  💡 Jas -> 🎨 Barva -> 🔄 Vzor")
print("Vzory:", ", ".join(PATTERNS))
print("Stiskněte Ctrl+C pro ukončení")
print()
print("⚙️ Mód: Jas")

while True:
    # Zpracuj vstupy
    handle_encoder()
    handle_button()
    
    # Zobraz aktuální vzor
    show_pattern()
    
    # Krátká pauza
    time.sleep(0.05)
