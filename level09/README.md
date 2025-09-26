# Level 9 - Alarm s fotorezistorem

## Popis
Přidání světelného senzoru pro vytvoření jednoduchého alarmu. Naučíte se číst analogové hodnoty a reagovat na změny světla.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 8 a přidáváme modul s fotorezistorem:
- **PONECHÁVÁME:** Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

- **PŘIDÁVÁME:** Modul s fotorezistorem KY-018 připojte (pozor, některé moduly mají jiné zapojení):
  - Middle (střední pin) k 3V3 nebo 5V (napájení)
  - - (minus) k zemi (GND)
  - S (signál) k analogovému vstupu A1

## Co se naučíte
- Fotorezistor jako světelný senzor
- Analogové čtení světelných hodnot
- Porovnání s prahem (threshold)
- Jednoduchý alarm systém
- Praktické použití světelného senzoru

## Soubory
- `code.py` - Světelný alarm s pípáním při zatmění senzoru
