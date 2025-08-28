"""
LEVEL 11B - Čtení teploty z DS18B20 senzoru (OneWire)

ZAPOJENÍ OBVODU:
- DS18B20 modul připojte:
  - VDD k 3V3
  - GND k zemi (GND)
  - DQ k GP22

JAK FUNGUJE ONEWIRE:
OneWire je komunikační protokol, který používá pouze jeden datový vodič (DQ).
Data se posílají sériově - bit po bitu. Senzory mají jedinečnou adresu,
takže na jednu linku můžete připojit více senzorů DS18B20.

NOVÉ KONCEPTY:
- OneWire protokol - komunikace jedním vodičem
- Digitální teplotní senzor DS18B20 (±0.5°C)
- Možnost připojení více senzorů na jednu linku
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import digitalio       # práce s digitálními vstupy a výstupy
import time            # funkce pro čekání a práci s časem
import adafruit_onewire.bus   # OneWire komunikační protokol
import adafruit_ds18x20       # knihovna pro DS18B20/DS18S20 senzory

# vytvoření OneWire sběrnice na GP22
ow_bus = adafruit_onewire.bus.OneWireBus(board.GP22)

print("🌡️  DS18B20 SENZOR")
print("Hledání senzorů na OneWire sběrnici...")

# vyhledání všech DS18x20 senzorů na sběrnici
devices = ow_bus.scan()
print(f"Nalezeno {len(devices)} senzorů")

# vytvoření objektů pro všechny nalezené senzory
senzory = []
for device in devices:
    senzor = adafruit_ds18x20.DS18X20(ow_bus, device)
    senzory.append(senzor)

print("Teplota každé 3 sekundy:")
print()

# hlavní smyčka čtení teploty
while True:
    # čtení ze všech senzorů
    for i, senzor in enumerate(senzory):
        teplota = senzor.temperature
        print(f"Senzor {i+1}: {teplota:.1f}°C")
    
    # čekání 3 sekundy
    time.sleep(3)
