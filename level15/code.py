"""
LEVEL 15 - NeoPixel Matrix + Akcelerometr - Kulička na náklonu

ZAPOJENÍ OBVODU:
Kombinujeme hardware z Level 13 a Level 14:

1) NeoPixel matrix 4x4:
   - VCC k 3V3 nebo 5V
   - GND k zemi (GND)
   - DIN k GP18

2) MPU6500/MPU6050 akcelerometr (I2C):
   - VCC k 3V3
   - GND k zemi (GND)
   - SDA k GP16 (I2C data - modrá)
   - SCL k GP17 (I2C clock - žlutá)

3) Pasivní bzučák (pro pípání při nárazu):
   - Kladný pin k GP06
   - Záporný pin k zemi (GND)

JAK FUNGUJE HRA:
Jednoduchá fyzikální simulace kuličky na nakloněné desce:
- Kulička (LED) se pohybuje podle náklonu Pico
- Nakloníte-li Pico doprava → kulička se valí doprava
- Nakloníte-li Pico doleva → kulička se valí doleva
- Kulička se zastaví na okrajích matice
- Při nárazu na stěnu se přehraje krátké pípnutí

HERNÍ MECHANIKA:
- Červená LED = kulička
- Pozice kuličky se aktualizuje podle akcelerometru
- Plynulý pohyb s fyzikou (rychlost, zrychlení, tření)
- Zastavení na okrajích matice (bez odrazu)
- Zvuková zpětná vazba při nárazu

NOVÉ KONCEPTY:
- Spojení senzoru s výstupem (input → processing → output)
- Herní smyčka (game loop)
- Základní fyzika (pozice, rychlost, zrychlení)
- Mapování hodnot senzoru na herní svět
- Interaktivní zpětná vazba
- Zvuková indikace událostí
"""

# import knihoven pro práci s hardware
import board                           # přístup k pinům a hardware zařízení
import busio                           # I2C komunikace
import neopixel                        # knihovna pro NeoPixel LED
import time                            # funkce pro čekání a práci s časem
import simpleio                        # modul pro jednoduché tóny
import makerclass_accelerometer        # naše univerzální knihovna pro MPU senzory

# konfigurace hardware
NEOPIXEL_PIN = board.GP18
NUM_PIXELS = 16
BRIGHTNESS = 0.3
BUZZER_PIN = board.GP6                # pin pro bzučák

# vytvoření objektů
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)
i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA
mpu = makerclass_accelerometer.MakerClassAccelerometer(i2c)

# herní konstanty
MATRIX_SIZE = 4                    # velikost matice (4x4)
BALL_COLOR = (255, 0, 0)         # červená kulička
BLACK = (0, 0, 0)                 # prázdné místo

# herní proměnné
ball_x = 2.0                      # pozice kuličky X (float pro plynulost)
ball_y = 2.0                      # pozice kuličky Y (float pro plynulost)
ball_vel_x = 0.0                  # rychlost kuličky X
ball_vel_y = 0.0                  # rychlost kuličky Y

# stav kuličky u zdi
was_at_left_wall = False          # byla kulička u levé stěny
was_at_right_wall = False         # byla kulička u pravé stěny
was_at_top_wall = False           # byla kulička u horní stěny
was_at_bottom_wall = False        # byla kulička u dolní stěny

# fyzikální konstanty
SENSITIVITY = 15.0                # citlivost na náklon
FRICTION = 0.85                   # tření (zpomalování)
MIN_VELOCITY = 0.01               # minimální rychlost (zastavení)

# konstanty pro pípání při nárazu
BUMP_FREQUENCY = 600              # frekvence pípnutí při nárazu (Hz)
BUMP_DURATION = 0.05              # délka pípnutí (sekundy)

def clear_matrix():
    """Vyčistí celou matici"""
    pixels.fill(BLACK)

def set_pixel(x, y, color):
    """Nastaví pixel na pozici x, y (0-3)"""
    if 0 <= x < MATRIX_SIZE and 0 <= y < MATRIX_SIZE:
        # Mapování 2D souřadnic na 1D index
        if y % 2 == 0:  # sudé řádky - zleva doprava
            index = y * MATRIX_SIZE + x
        else:           # liché řádky - zprava doleva
            index = y * MATRIX_SIZE + (MATRIX_SIZE - 1 - x)
        
        pixels[index] = color

def update_physics():
    """Aktualizuje fyziku kuličky podle akcelerometru"""
    global ball_x, ball_y, ball_vel_x, ball_vel_y
    global was_at_left_wall, was_at_right_wall, was_at_top_wall, was_at_bottom_wall
    
    # Čtení akcelerometru
    accel_x, accel_y, accel_z = mpu.acceleration
    
    # Mapování náklonu na sílu (správné směry)
    force_x = accel_y / SENSITIVITY   # náklon doprava/doleva
    force_y = -accel_x / SENSITIVITY  # náklon dopředu/dozadu
    
    # Aplikace síly na rychlost
    ball_vel_x += force_x
    ball_vel_y += force_y
    
    # Aplikace tření
    ball_vel_x *= FRICTION
    ball_vel_y *= FRICTION
    
    # Zastavení při velmi malé rychlosti
    if abs(ball_vel_x) < MIN_VELOCITY:
        ball_vel_x = 0
    if abs(ball_vel_y) < MIN_VELOCITY:
        ball_vel_y = 0
    
    # Aktualizace pozice
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    
    # Omezení na hranice matice a detekce nárazu
    bumped = False  # příznak nárazu
    
    # Levá stěna (X = 0)
    if ball_x < 0:
        ball_x = 0
        ball_vel_x = 0
        if not was_at_left_wall:  # nový náraz
            bumped = True
        was_at_left_wall = True
    else:
        was_at_left_wall = False
    
    # Pravá stěna (X = 3)
    if ball_x >= MATRIX_SIZE - 1:
        ball_x = MATRIX_SIZE - 1
        ball_vel_x = 0
        if not was_at_right_wall:  # nový náraz
            bumped = True
        was_at_right_wall = True
    else:
        was_at_right_wall = False
    
    # Horní stěna (Y = 0)
    if ball_y < 0:
        ball_y = 0
        ball_vel_y = 0
        if not was_at_top_wall:  # nový náraz
            bumped = True
        was_at_top_wall = True
    else:
        was_at_top_wall = False
    
    # Dolní stěna (Y = 3)
    if ball_y >= MATRIX_SIZE - 1:
        ball_y = MATRIX_SIZE - 1
        ball_vel_y = 0
        if not was_at_bottom_wall:  # nový náraz
            bumped = True
        was_at_bottom_wall = True
    else:
        was_at_bottom_wall = False
    
    # Pípnutí při novém nárazu na stěnu
    if bumped:
        simpleio.tone(BUZZER_PIN, BUMP_FREQUENCY, BUMP_DURATION)

def render_game():
    """Vykreslí herní scénu"""
    # Vyčisti matici
    clear_matrix()
    
    # Zobraz kuličku na aktuální pozici
    pixel_x = int(round(ball_x))
    pixel_y = int(round(ball_y))
    set_pixel(pixel_x, pixel_y, BALL_COLOR)
    
    # Aktualizuj displej
    pixels.show()

def print_debug_info():
    """Vypíše debug informace o stavu hry"""
    accel_x, accel_y, accel_z = mpu.acceleration
    debug_text = f"Pozice: ({ball_x:.1f}, {ball_y:.1f}) | Rychlost: ({ball_vel_x:.2f}, {ball_vel_y:.2f}) | Akcelerometr: X:{accel_x:.1f} Y:{accel_y:.1f}"
    print(debug_text)

print("🎮 KULIČKA NA NÁKLONU")
print("Nakláněním Pico ovládáte červenou kuličku")
print("Kulička se zastaví na okrajích matice")
print("Pozice kuličky a rychlost se zobrazují v konzoli")
print()

# herní smyčka
frame_count = 0
while True:
    # Aktualizuj fyziku
    update_physics()
    
    # Vykresli hru
    render_game()
    
    # Debug info každých 10 snímků (snížení spamu v konzoli)
    if frame_count % 10 == 0:
        print_debug_info()
    
    frame_count += 1
    
    # Herní snímková frekvence (cca 20 FPS)
    time.sleep(0.05)
