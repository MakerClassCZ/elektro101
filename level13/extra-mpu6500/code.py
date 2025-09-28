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

NOVÉ KONCEPTY:
- MPU6500 senzor (vylepšený MPU6050)
- Přímé čtení I2C registrů
- Převod raw dat na fyzikální hodnoty
- Kalibrace a škálování senzorů
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import busio           # I2C komunikace
import time            # funkce pro čekání a práci s časem
import struct          # pro převod binárních dat
import displayio       # základní grafické operace
import terminalio      # vestavěný font
import adafruit_displayio_ssd1306  # knihovna pro SSD1306 OLED
from adafruit_display_text import label  # textové popisky

class MPU6500:
    """Jednoduchá třída pro práci s MPU6500"""
    
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        
        # inicializace senzoru
        self._write_register(0x6B, 0x00)  # wakeup (reset sleep mode)
        time.sleep(0.1)
        self._write_register(0x1C, 0x00)  # akcelerometr ±2g
        self._write_register(0x1B, 0x00)  # gyroskop ±250°/s
        
    def _write_register(self, register, value):
        """Zapíše hodnotu do registru"""
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.address, bytes([register, value]))
        finally:
            self.i2c.unlock()
    
    def _read_register(self, register, length=1):
        """Přečte hodnotu z registru"""
        while not self.i2c.try_lock():
            pass
        try:
            result = bytearray(length)
            self.i2c.writeto_then_readfrom(self.address, bytes([register]), result)
            return result
        finally:
            self.i2c.unlock()
    
    def _read_word_2c(self, register):
        """Přečte 16-bit hodnotu se znaménkem"""
        data = self._read_register(register, 2)
        value = struct.unpack('>h', data)[0]  # big-endian signed 16-bit
        return value
    
    @property
    def acceleration(self):
        """Vrátí zrychlení v m/s² (X, Y, Z)"""
        accel_x = self._read_word_2c(0x3B)
        accel_y = self._read_word_2c(0x3D)
        accel_z = self._read_word_2c(0x3F)
        
        # převod na m/s² (±2g range, 16384 LSB/g)
        scale = 9.81 / 16384.0
        return (accel_x * scale, accel_y * scale, accel_z * scale)
    
    @property
    def gyro(self):
        """Vrátí úhlovou rychlost v rad/s (X, Y, Z)"""
        gyro_x = self._read_word_2c(0x43)
        gyro_y = self._read_word_2c(0x45)
        gyro_z = self._read_word_2c(0x47)
        
        # převod na rad/s (±250°/s range, 131 LSB/°/s)
        import math
        scale = math.radians(1.0 / 131.0)
        return (gyro_x * scale, gyro_y * scale, gyro_z * scale)
    
    @property
    def temperature(self):
        """Vrátí teplotu v °C"""
        temp_raw = self._read_word_2c(0x41)
        # převod podle datasheetu: Temperature = (TEMP_OUT / 340.0) + 36.53
        return (temp_raw / 340.0) + 36.53

# vytvoření I2C sběrnice (sdílená pro MPU6500 i OLED)
i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA

# inicializace MPU6500 senzoru
mpu = MPU6500(i2c)

# inicializace OLED displeje
displayio.release_displays()  # uvolnění případných předchozích displejů
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

print("🎮 MPU6500 + OLED DISPLEJ")
print("Zobrazení dat z gyroskopu a akcelerometru")
print("I2C adresy: MPU6500=0x68, SSD1306=0x3C")
print()

# vytvoření skupiny pro zobrazení textu
main_group = displayio.Group()

# vytvoření textových popisků pro data - všechny 3 osy
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
        # čtení dat z MPU6500
        accel_x_val, accel_y_val, accel_z_val = mpu.acceleration  # m/s²
        gyro_x_val, gyro_y_val, gyro_z_val = mpu.gyro            # rad/s
        teplota = mpu.temperature                                  # °C
        
        # převod gyro z rad/s na °/s pro lepší pochopení
        import math
        gyro_x_deg = math.degrees(gyro_x_val)
        gyro_y_deg = math.degrees(gyro_y_val)
        gyro_z_deg = math.degrees(gyro_z_val)
        
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
