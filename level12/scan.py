"""
LEVEL 12 - I2C Scanner

ZAPOJENÍ OBVODU:
Připojte jakákoliv I2C zařízení na sběrnici:
- SDA k GP16 (modrá)
- SCL k GP17 (žlutá)
- VCC k 3V3
- GND k GND

JAK FUNGUJE I2C SKENOVÁNÍ:
Tento skript projde všechny možné I2C adresy (0x08-0x77) a pokusí se
s každou komunikovat. Pokud zařízení odpoví, vypíše jeho adresu.
Každé I2C zařízení má unikátní adresu - SHT40 má 0x44, SSD1306 má 0x3C.

NOVÉ KONCEPTY:
- Skenování I2C sběrnice
- I2C adresy zařízení (hexadecimálně)
- Detekce připojených zařízení
- Try/except pro testování komunikace
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import busio           # I2C komunikace
import time            # funkce pro čekání a práci s časem

print("🔍 I2C SCANNER")
print("Skenování I2C sběrnice na GP16/GP17...")
print()

# vytvoření I2C sběrnice
i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA

try:
    # čekání na inicializaci I2C
    while not i2c.try_lock():
        pass
    
    print("Skenování adres 0x08 - 0x77...")
    print()
    
    # seznam nalezených zařízení
    nalezena_zarizeni = []
    
    # skenování všech možných I2C adres
    for adresa in range(0x08, 0x78):  # standardní rozsah I2C adres
        try:
            # pokus o komunikaci s adresou
            i2c.writeto(adresa, b'')
            
            # pokud nedošlo k chybě, zařízení odpovědělo
            hex_adresa = hex(adresa)
            print(f"✅ Nalezeno zařízení na adrese: {hex_adresa} ({adresa})")
            nalezena_zarizeni.append((hex_adresa, adresa))
            
        except OSError:
            # žádné zařízení na této adrese
            pass
    
    print()
    print(f"Skenování dokončeno!")
    print(f"Nalezeno celkem: {len(nalezena_zarizeni)} zařízení")
    
    if nalezena_zarizeni:
        print()
        print("📋 SEZNAM NALEZENÝCH ZAŘÍZENÍ:")
        for hex_addr, dec_addr in nalezena_zarizeni:
            # rozpoznání známých zařízení podle adresy
            if dec_addr == 0x44:
                nazev = "SHT40 (teplota/vlhkost)"
            elif dec_addr in [0x3C, 0x3D]:
                nazev = "SSD1306 (OLED displej)"
            elif dec_addr == 0x76 or dec_addr == 0x77:
                nazev = "BME280/BMP280 (tlak/teplota)"
            elif dec_addr == 0x48:
                nazev = "ADS1115 (ADC)"
            elif dec_addr == 0x68:
                nazev = "MPU6050/GY-521 (IMU 6-axis)"
            elif dec_addr == 0x69:
                nazev = "MPU6050/GY-521 (IMU 6-axis, alt. adresa)"
            elif dec_addr == 0x40:
                nazev = "PCA9685 (PWM driver)"
            else:
                nazev = "Neznámé zařízení"
            
            print(f"  • {hex_addr}: {nazev}")
    else:
        print()
        print("❌ Žádná zařízení nenalezena!")
        print()
        print("Možné příčiny:")
        print("- Žádná I2C zařízení nejsou připojena")
        print("- Špatné zapojení SDA/SCL")
        print("- Chybí napájení zařízení")
        print("- Chybí pull-up odpory (obvykle jsou na modulech)")

finally:
    # uvolnění I2C sběrnice
    i2c.unlock()
    i2c.deinit()
    print()
    print("I2C sběrnice uvolněna")
