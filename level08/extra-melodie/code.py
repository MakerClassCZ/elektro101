"""
LEVEL 8 - Přehrávání melodií rotačním enkodérem (SIMPLEIO VERZE)

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 6 a nahrazujeme servo bzučákem:
- PONECHÁVÁME: Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN
  - DT k digitálnímu vstupu GP04 (A pin) 
  - CLK k digitálnímu vstupu GP03 (B pin)
  - SW připojte k GP02 (tlačítko play)

- PŘIDÁVÁME: Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

- PŘIDÁVÁME: LED indikátor připojte:
  - Anoda (+) k GP00
  - Katoda (-) přes odpor 330Ω k zemi (GND)

Toto je vylepšená verze používající modul simpleio pro přehrávání
melodií a jednotlivých tónů s přesným časováním.

VYLEPŠENÍ:
- Použití simpleio.tone() pro přehrávání tónů
- Předefinované melodie
- Enkodér pro výběr melodie
- Tlačítko pro spuštění vybrané melodie
- LED indikátor při přehrávání melodie
- Jednodušší API než manuální PWM
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import rotaryio     # vestavěný modul pro rotační enkodéry
import digitalio    # práce s digitálními vstupy (tlačítko)
import simpleio     # modul pro jednoduché tóny a melodie
import time         # funkce pro čekání a práci s časem

# vytvoření objektu pro enkodér
encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3)

# vytvoření objektu pro tlačítko
button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# vytvoření objektu pro LED indikátor
led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

# proměnné pro sledování enkodéru a tlačítka
posledni_pozice = 0
aktualni_melodie = 0
posledni_stav_tlacitka = True

# hudební noty (frekvence v Hz, zaokrouhlené na integery)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523
D5 = 587
E5 = 659
F5 = 698
G5 = 784

# délka tónů (vizuální reprezentace)
O = 0.2      # krátká nota
OO = 0.4     # střední nota  
OOO = 0.6    # dlouhá nota
X = 0    # pauza (žádný tón)

# definice melodií (nota, délka)
melodie = [
    {
        "nazev": "Tvinkle Twinkle",
        "tony": [
            (C4, OO), (C4, OO), (G4, OO), (G4, OO),
            (A4, OO), (A4, OO), (G4, OOO), (X, O),
            (F4, OO), (F4, OO), (E4, OO), (E4, OO),
            (D4, OO), (D4, OO), (C4, OOO)
        ]
    },
    {
        "nazev": "Mary Had a Little Lamb",
        "tony": [
            (E4, OO), (D4, OO), (C4, OO), (D4, OO),
            (E4, OO), (E4, OO), (E4, OOO), (X, O),
            (D4, OO), (D4, OO), (D4, OOO), (X, O),
            (E4, OO), (G4, OO), (G4, OOO)
        ]
    },
    {
        "nazev": "Happy Birthday",
        "tony": [
            (C4, O), (C4, O), (D4, OO), (C4, OO),
            (F4, OO), (E4, OOO), (X, O),
            (C4, O), (C4, O), (D4, OO), (C4, OO),
            (G4, OO), (F4, OOO)
        ]
    },
    {
        "nazev": "Škály C dur",
        "tony": [
            (C4, O), (D4, O), (E4, O), (F4, O),
            (G4, O), (A4, O), (B4, O), (C5, OO), (X, O),
            (C5, O), (B4, O), (A4, O), (G4, O),
            (F4, O), (E4, O), (D4, O), (C4, OO)
        ]
    },
    {
        "nazev": "Indiana Jones (Raiders March)",
        "tony": [
            (E4, O), (F4, O), (G4, OO), (C5, OOO), (X, O),
            (D4, O), (E4, O), (F4, OOO), (X, O),
            (G4, O), (A4, O), (B4, OO), (F5, OOO), (X, O),
            (A4, O), (B4, O), (C5, OO), (D5, OO), (E5, OO)
        ]
    }
]

def prehraj_melodii(melodie_data):
    """Přehraje melodii pomocí simpleio.tone() s LED indikátorem"""
    print(f"Přehrávám: {melodie_data['nazev']}")
    
    for nota, delka in melodie_data["tony"]:
        if nota == X:
            # pauza - LED zhasne, pouze čekání bez zvuku
            led.value = False
            time.sleep(delka)
        else:
            # přehrání tónu s LED
            led.value = True  # rozsvícení LED
            simpleio.tone(board.GP6, nota, delka)
            led.value = False  # zhasnutí LED
        
        # krátká pauza mezi tóny (kromě explicitních pauz)
        if nota != X:
            time.sleep(0.05)
    
    # ujistit se, že LED je zhasnuta na konci
    led.value = False
    print("Melodie dokončena")

print("🎵 MUSIC PLAYER 🎵")
print("Otáčejte enkodérem pro výběr melodie")
print("Stiskněte tlačítko pro přehrání")
print(f"Dostupné melodie: {len(melodie)}")

# výpis dostupných melodií
for i, mel in enumerate(melodie):
    print(f"  {i+1}. {mel['nazev']}")

print(f"\n>>> Vybrána: {melodie[aktualni_melodie]['nazev']} <<<")
print("Stiskněte tlačítko pro přehrání")

# hlavní smyčka
while True:
    # čtení pozice enkodéru
    aktualni_pozice = encoder.position
    
    # kontrola změny pozice enkodéru
    if aktualni_pozice != posledni_pozice:
        # výpočet rozdílu
        rozdil = aktualni_pozice - posledni_pozice
        
        # změna melodie podle směru otáčení
        if rozdil > 0:
            # otáčení vpravo - další melodie
            aktualni_melodie = (aktualni_melodie + 1) % len(melodie)
        elif rozdil < 0:
            # otáčení vlevo - předchozí melodie
            aktualni_melodie = (aktualni_melodie - 1) % len(melodie)
        
        # výpis vybrané melodie
        print(f"\n>>> Vybrána: {melodie[aktualni_melodie]['nazev']} <<<")
        print("Stiskněte tlačítko pro přehrání")
        
        # uložení pozice
        posledni_pozice = aktualni_pozice
    
    # kontrola tlačítka
    aktualni_stav_tlacitka = button.value
    
    # detekce stisku tlačítka (změna z True na False)
    if posledni_stav_tlacitka == True and aktualni_stav_tlacitka == False:
        print(f"\n🎶 PŘEHRÁVÁM: {melodie[aktualni_melodie]['nazev']} 🎶")
        prehraj_melodii(melodie[aktualni_melodie])
        print("Melodie dokončena. Vyberte další a stiskněte tlačítko.")
        
        # krátká pauza proti "poskakování" tlačítka
        time.sleep(0.2)
    
    # uložení stavu tlačítka
    posledni_stav_tlacitka = aktualni_stav_tlacitka
    
    # krátká pauza
    time.sleep(0.01)
