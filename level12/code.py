"""
LEVEL 12 - OLED Display s teplotním senzorem SHT40

ZAPOJENÍ OBVODU:
Na I2C sběrnici připojíme dva moduly:

1) SHT40 senzor teploty a vlhkosti:
   - VDD k 3V3
   - GND k zemi (GND)
   - SDA k GP16 (I2C data - modrá)
   - SCL k GP17 (I2C clock - žlutá)

2) OLED Display SSD1306 128x64:
 - Připojený  na sběrnici pomocí uŠup

JAK FUNGUJE I2C S VÍCE ZAŘÍZENÍMI:
Krása I2C protokolu je v tom, že na jednu sběrnici můžeme připojit více
zařízení. Každé má unikátní adresu:
- SHT40 má adresu 0x44
- SSD1306 má obvykle adresu 0x3C nebo 0x3D
Master (Pico) komunikuje s každým zvlášť podle adresy.

NOVÉ KONCEPTY:
- OLED display SSD1306 (128x64 pixelů)
- Více zařízení na jedné I2C sběrnici
- Textové zobrazení na displeji
- Knihovna displayio pro grafiku
- Kombinace senzoru a displeje
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import busio           # I2C komunikace
import time            # funkce pro čekání a práci s časem
import displayio       # základní grafické operace
import terminalio      # vestavěný font
import adafruit_displayio_ssd1306  # knihovna pro SSD1306 OLED
import adafruit_sht4x  # knihovna pro SHT40 senzor
from adafruit_display_text import label  # textové popisky

# vytvoření I2C sběrnice (sdílená pro SHT40 i OLED)
i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA

# inicializace SHT40 senzoru
sht = adafruit_sht4x.SHT4x(i2c)

# inicializace OLED displeje
displayio.release_displays()  # uvolnění případných předchozích displejů
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

print("🌡️📺 SHT40 + OLED DISPLEJ")
print("Zobrazení teploty a vlhkosti na OLED displeji")
print("I2C piny: SDA=GP16, SCL=GP17")
print("I2C adresy: SHT40=0x44, SSD1306=0x3C")
print()

# vytvoření skupiny pro zobrazení textu
main_group = displayio.Group()

# vytvoření textových popisků
title_label = label.Label(terminalio.FONT, text="SHT40 Senzor", color=0xFFFFFF, x=25, y=10)
temp_label = label.Label(terminalio.FONT, text="Teplota:", color=0xFFFFFF, x=5, y=25)
temp_value = label.Label(terminalio.FONT, text="--.-°C", color=0xFFFFFF, x=70, y=25)
hum_label = label.Label(terminalio.FONT, text="Vlhkost:", color=0xFFFFFF, x=5, y=40)
hum_value = label.Label(terminalio.FONT, text="--.-%", color=0xFFFFFF, x=70, y=40)
time_label = label.Label(terminalio.FONT, text="00:00", color=0xFFFFFF, x=85, y=55)

# přidání všech popisků do skupiny
main_group.append(title_label)
main_group.append(temp_label)
main_group.append(temp_value)
main_group.append(hum_label)
main_group.append(hum_value)
main_group.append(time_label)

# zobrazení skupiny na displeji
display.root_group = main_group

# proměnné pro čas
start_time = time.monotonic()

# hlavní smyčka zobrazování dat
try:
    while True:
        # čtení teploty a vlhkosti z SHT40
        teplota = sht.temperature
        vlhkost = sht.relative_humidity
        
        # aktualizace textů na displeji
        temp_value.text = f"{teplota:.1f}°C"
        hum_value.text = f"{vlhkost:.1f}%"
        
        # přesné počítání času pomocí monotonic
        uplynuly_cas = time.monotonic() - start_time
        minuty = int(uplynuly_cas) // 60
        sekundy = int(uplynuly_cas) % 60
        time_label.text = f"{minuty:02d}:{sekundy:02d}"
        
        # zobrazení dat také v konzoli
        print(f"Teplota: {teplota:.1f}°C, Vlhkost: {vlhkost:.1f}%, Čas: {minuty:02d}:{sekundy:02d}")
        
        # čekání 1 sekundu
        time.sleep(1)

finally: 
    i2c.deinit()
    print("I2C sběrnice uvolněna")
