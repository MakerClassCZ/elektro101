"""
LEVEL 7 - Ovládání servo motoru SG90 ze sériové konzole

ZAPOJENÍ OBVODU:
- Servo motor SG90 připojte:
  - Červený vodič (VCC) k 5V nebo externímu napájení
  - Černý/hnědý vodič (GND) k zemi (GND)
  - Oranžový/žlutý vodič (SIGNAL) k GP05

Zadejte číslo 0-180 pro nastavení úhlu serva.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import simpleio     # jednoduché IO operace včetně serva

# vytvoření servo objektu pomocí simpleio knihovny
my_servo = simpleio.Servo(board.GP5)

# nastavení serva na počáteční pozici (střed)
my_servo.angle = 90

print("Servo ovládání - zadejte úhel (0-180):")

# hlavní smyčka
while True:
    # čtení vstupu ze sériové konzole
    vstup = input("Úhel: ").strip()
    
    # prázdný vstup - opakovat
    if not vstup:
        continue
    
    # převod na číslo
    uhel = int(vstup)
    
    # validace rozsahu
    if uhel < 0 or uhel > 180:
        print("Úhel musí být 0-180")
        continue
    
    # nastavení serva
    my_servo.angle = uhel
    print(f"Servo: {uhel}°")
