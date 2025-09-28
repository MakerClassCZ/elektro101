"""
LEVEL 11D - Čtení teploty a vlhkosti z SHT40 senzoru (I2C)

ZAPOJENÍ OBVODU:
- SHT40 modul připojte:
  - VDD k 3V3
  - GND k zemi (GND)
  - SDA k GP16 (I2C data)
  - SCL k GP17 (I2C clock)

JAK FUNGUJE I2C:
I2C (Inter-Integrated Circuit) je dvouvodičový sériový protokol. SDA přenáší
data, SCL poskytuje hodinový signál. Každé zařízení má unikátní adresu.
Master (Pico) může komunikovat s více Slave zařízeními (senzory) na stejné
sběrnici. Data se posílají po bajtech s ACK/NACK potvrzením.

NOVÉ KONCEPTY:
- I2C protokol - dvouvodičová sériová komunikace
- Master/Slave architektura
- Velmi přesný senzor SHT40 (±0.2°C, ±1.8% RH)
- Adresování zařízení na I2C sběrnici
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import busio           # I2C komunikace
import time            # funkce pro čekání a práci s časem
import adafruit_sht4x  # knihovna pro SHT40 senzor

# vytvoření I2C sběrnice a SHT40 senzoru
i2c = busio.I2C(board.GP17, board.GP16)  # SCL, SDA
sht = adafruit_sht4x.SHT4x(i2c)

print("🌡️💧 SHT40 SENZOR")
print("Velmi přesná teplota a vlhkost každé 2 sekundy:")
print()

# hlavní smyčka čtení teploty a vlhkosti
while True:
    # čtení teploty a vlhkosti z SHT40
    teplota = sht.temperature
    vlhkost = sht.relative_humidity
    
    # zobrazení hodnot
    print(f"Teplota: {teplota:.2f}°C, Vlhkost: {vlhkost:.1f}%")
    
    # čekání 2 sekundy
    time.sleep(2)
