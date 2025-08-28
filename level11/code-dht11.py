"""
LEVEL 11C - Čtení teploty a vlhkosti z DHT11/DHT22 senzoru

ZAPOJENÍ OBVODU:
- DHT11/DHT22 modul připojte:
  - VCC k 3V3
  - DATA k GP21
  - GND k zemi (GND)

JAK FUNGUJE DHT KOMUNIKACE:
DHT senzory používają vlastní jednovodičový protokol. Mikrokontrolér pošle
startovací signál, senzor odpověe 40 bity dat (16 bit vlhkost + 16 bit teplota 
+ 8 bit kontrolní součet). Timing je kritický - proto potřebují delší pauzy
mezi měřeními.

NOVÉ KONCEPTY:
- Kombinovaný senzor teploty a vlhkosti
- Relativní vlhkost vzduchu (RH %)
- Jednovodičový protokol s přesným timingem
- DHT11 (±2°C, ±5% RH) vs DHT22 (±0.5°C, ±2-5% RH)
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import time            # funkce pro čekání a práci s časem
import adafruit_dht    # knihovna pro DHT11/DHT22 senzory

# vytvoření DHT objektu na GP21
# Zkuste nejdříve DHT22, pokud nefunguje, změňte na DHT11
dht = adafruit_dht.DHT22(board.GP21)
# dht = adafruit_dht.DHT11(board.GP21)  # použijte pro DHT11

print("🌡️💧 DHT11/DHT22 SENZOR")
print("Teplota a vlhkost každých 5 sekund:")
print()

# hlavní smyčka čtení teploty a vlhkosti
while True:
    # čtení teploty a vlhkosti z DHT senzoru
    teplota = dht.temperature
    vlhkost = dht.humidity
    
    # zobrazení hodnot
    if teplota is not None and vlhkost is not None:
        print(f"Teplota: {teplota:.1f}°C, Vlhkost: {vlhkost:.1f}%")
    else:
        print("Chyba čtení")
    
    # čekání 5 sekund (DHT potřebuje delší pauzy)
    time.sleep(5)
