"""
LEVEL 13 - MPU6500 Gyroscope/Accelerometer s OLED displayem

ZAPOJENÍ OBVODU:
Na I2C sběrnici připojíme dva moduly:

1) GY-521 MPU6500 IMU senzor:
   - VCC k 3V3
   - GND k zemi (GND)
   - SCL k GP17 (I2C clock - žlutá)
   - SDA k GP16 (I2C data - modrá)

2) OLED Display SSD1306 128x64:
   - VCC k 3V3
   - GND k zemi (GND)  
   - SDA k GP16 (I2C data - modrá) - SDÍLENO
   - SCL k GP17 (I2C clock - žlutá) - SDÍLENO

JAK FUNGUJE MPU6500:
MPU6500 je vylepšená verze MPU6050. Je 6-axis IMU obsahující:
- 3-axis akcelerometr (měří zrychlení/gravitaci v osách X,Y,Z)
- 3-axis gyroskop (měří úhlovou rychlost otáčení)
- Vestavěný teplotní senzor (WHO_AM_I = 0x70)
Data se čtou přes I2C na adrese 0x68 nebo 0x69.

NOVÉ KONCEPTY:
- MPU6500 senzor (vylepšený MPU6050)
- Akcelerometr - měření zrychlení a gravitace
- Gyroskop - měření úhlové rychlosti  
- 6-axis snímání pohybu
- Kombinace více senzorů na I2C
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import busio           # I2C komunikace
import time            # funkce pro čekání a práci s časem
import math            # matematické funkce
import displayio       # základní grafické operace
import terminalio      # vestavěný font
import adafruit_displayio_ssd1306  # knihovna pro SSD1306 OLED
import makerclass_accelerometer  # MakerClass univerzální knihovna pro MPU senzory
from adafruit_display_text import label  # textové popisky

# vytvoření I2C sběrnice (sdílená pro MPU senzor i OLED)
i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA

# inicializace MPU senzoru (automatická detekce MPU6050/MPU6500/MPU9250)
mpu = makerclass_accelerometer.MakerClassAccelerometer(i2c)

# inicializace OLED displeje
displayio.release_displays()  # uvolnění případných předchozích displejů
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

print("🎮 MPU SENZOR + OLED DISPLEJ")
print("Zobrazení dat z gyroskopu a akcelerometru")
print("I2C adresy: MPU=0x68, SSD1306=0x3C")
print()

# vytvoření skupiny pro zobrazení textu
main_group = displayio.Group()

# vytvoření textových popisků pro data - původní rozložení s 3 osami
title_label = label.Label(terminalio.FONT, text="MPU6500 IMU", color=0xFFFFFF, x=30, y=8)
accel_label = label.Label(terminalio.FONT, text="Accel:", color=0xFFFFFF, x=2, y=20)
accel_x = label.Label(terminalio.FONT, text="X:0.0", color=0xFFFFFF, x=2, y=30)
accel_y = label.Label(terminalio.FONT, text="Y:0.0", color=0xFFFFFF, x=45, y=30)
accel_z = label.Label(terminalio.FONT, text="Z:0.0", color=0xFFFFFF, x=88, y=30)
gyro_label = label.Label(terminalio.FONT, text="Gyro:", color=0xFFFFFF, x=2, y=42)
gyro_x = label.Label(terminalio.FONT, text="X:0.0", color=0xFFFFFF, x=2, y=52)
gyro_y = label.Label(terminalio.FONT, text="Y:0.0", color=0xFFFFFF, x=45, y=52)
gyro_z = label.Label(terminalio.FONT, text="Z:0.0", color=0xFFFFFF, x=88, y=52)

# přidání všech popisků do skupiny
main_group.append(title_label)
main_group.append(accel_label)
main_group.append(accel_x)
main_group.append(accel_y)
main_group.append(accel_z)
main_group.append(gyro_label)
main_group.append(gyro_x)
main_group.append(gyro_y)
main_group.append(gyro_z)

# zobrazení skupiny na displeji
display.root_group = main_group

# hlavní smyčka čtení IMU dat
try:
    while True:
        # čtení dat z MPU senzoru (automaticky rozpoznán typ čipu)
        accel_x_val, accel_y_val, accel_z_val = mpu.acceleration  # m/s²
        gyro_x_val, gyro_y_val, gyro_z_val = mpu.gyro            # °/s
        teplota = mpu.temperature                                  # °C
        
        # data z gyroskopu jsou už ve stupních/s
        gyro_x_deg = gyro_x_val
        gyro_y_deg = gyro_y_val
        gyro_z_deg = gyro_z_val
        
        # aktualizace textů na displeji - všechny 3 osy
        accel_x.text = f"X:{accel_x_val:4.1f}"
        accel_y.text = f"Y:{accel_y_val:4.1f}"
        accel_z.text = f"Z:{accel_z_val:4.1f}"
        gyro_x.text = f"X:{gyro_x_deg:4.1f}"
        gyro_y.text = f"Y:{gyro_y_deg:4.1f}"
        gyro_z.text = f"Z:{gyro_z_deg:4.1f}"
        
        # zobrazení podrobných dat v konzoli
        print(f"Accel: X:{accel_x_val:5.2f} Y:{accel_y_val:5.2f} Z:{accel_z_val:5.2f} | Gyro: X:{gyro_x_deg:5.1f} Y:{gyro_y_deg:5.1f} Z:{gyro_z_deg:5.1f} | T:{teplota:.1f}°C")
        
        # čekání před dalším měřením
        time.sleep(0.2)

finally:
    # uvolnění I2C sběrnice
    i2c.deinit()
    print("I2C sběrnice uvolněna")