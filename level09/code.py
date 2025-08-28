"""
LEVEL 09 - Alarm s fotorezistorem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 08 a přidáváme modul s fotorezistorem:
- PONECHÁVÁME: Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

- PŘIDÁVÁME: Modul s fotorezistorem KY-018 připojte:
  - Middle (střední pin) k 3V3 nebo 5V (napájení)
  - - (minus) k zemi (GND)
  - S (signál) k analogovému vstupu A1

V tomto příkladu se naučíte číst hodnoty ze světelného senzoru (fotorezistoru)
a podle úrovně světla spouštět alarm. Když senzor zatměníte (např. rukou),
spustí se pípání - jednoduché světelné čidlo.

NOVÉ KONCEPTY:
- Fotorezistor jako světelný senzor
- Analogové čtení světelných hodnot
- Porovnání s prahem (threshold)
- Jednoduchý alarm systém
- Praktické použití světelného senzoru
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import analogio     # čtení analogových hodnot
import simpleio     # modul pro jednoduché tóny
import time         # funkce pro čekání a práci s časem

# vytvoření objektu pro fotorezistor na A1
fotorezistor = analogio.AnalogIn(board.A1)

# konstanty pro světelný alarm
SVETELNY_PRAH = 40000     # práh zatmění (při vyšší hodnotě = tma)
FREKVENCE_ALARM = 800     # frekvence alarmu
DELKA_PIP = 0.2           # délka jednoho pípnutí
PAUZA_ALARM = 0.3         # pauza mezi pípnutími alarmu

print("🔦 SVĚTELNÝ ALARM 🔦")
print(f"Práh zatmění: {SVETELNY_PRAH}")
print("Zatměte senzor rukou pro spuštění alarmu")
print("Váš KY-018: Světlo = nízké hodnoty, Tma = vysoké hodnoty")
print("Hodnoty senzoru pro diagnostiku:")


# hlavní smyčka světelného alarmu
while True:
    # čtení hodnoty ze světelného senzoru (0-65535)
    svetlo = fotorezistor.value
    
    # kontrola, zda je senzor zatměn (váš KY-018: vysoké hodnoty = tma)
    if svetlo > SVETELNY_PRAH:
        # senzor je zatměn - spustit alarm
        print(f"🚨 ALARM! Světlo: {svetlo:5d} (zatměno)")
        
        # pípnutí alarmu
        simpleio.tone(board.GP6, FREKVENCE_ALARM, DELKA_PIP)
        
        # pauza mezi pípnutími
        time.sleep(PAUZA_ALARM)
    else:
        # senzor vidí světlo - vše v pořádku
        print(f"✅ OK - Světlo: {svetlo:5d} (světlo)")
        
        # delší pauza když je klid
        time.sleep(0.5)