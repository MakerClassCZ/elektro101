# Level 10 - Parkovací senzor s ultrazvukovým čidlem HC-SR04

## Popis
Použití ultrazvukového senzoru pro měření vzdálenosti a vytvoření parkovacího senzoru. Naučíte se pracovat s časováním a mapováním hodnot.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 9 a přidáváme ultrazvukový senzor:
- **PONECHÁVÁME:** Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

- **PŘIDÁVÁME:** Ultrazvukový senzor HC-SR04 připojte:
  - VCC k 3V3 nebo 5V
  - GND k zemi (GND)  
  - TRIG k digitálnímu výstupu GP07 (spouštění měření)
  - ECHO k digitálnímu vstupu GP08 (příjem ozvěny)

## Co se naučíte
- Ultrazvukový senzor HC-SR04
- Měření vzdálenosti pomocí času ozvěny
- Knihovna `adafruit_hcsr04` pro CircuitPython
- Mapování vzdálenosti na rychlost pípání
- Parkovací senzor - praktická aplikace

## Soubory
- `code.py` - Parkovací senzor s rychlostí pípání podle vzdálenosti
