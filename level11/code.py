"""
LEVEL 11A - Čtení teploty z vestavěného senzoru RP2040

ZAPOJENÍ OBVODU:
Žádné externí zapojení není potřeba! RP2040 má vestavěný teplotní senzor.

JAK TO FUNGUJE:
Vestavěný senzor RP2040 měří teplotu přímo uvnitř čipu. Není příliš přesný 
(±2°C), ale je užitečný pro základní monitoring. Čteme ho pomocí jednoduché
funkce microcontroller.cpu.temperature.

NOVÉ KONCEPTY:
- Vestavěný teplotní senzor mikrokontroléru
- Přímé čtení teploty bez externí komunikace
- Monitoring teploty čipu
"""

# import knihoven pro práci s hardware
import board           # přístup k pinům a hardware zařízení
import microcontroller # přístup k funkcím mikrokontroléru
import time            # funkce pro čekání a práci s časem

print("🌡️  VESTAVĚNÝ SENZOR RP2040")
print("Teplota čipu každé 2 sekundy:")
print()

# hlavní smyčka čtení teploty
while True:
    # čtení teploty z vestavěného senzoru RP2040
    teplota = microcontroller.cpu.temperature
    
    # zobrazení teploty
    print(f"Teplota: {teplota:.1f}°C")
    
    # čekání 2 sekundy
    time.sleep(2)
