"""
LEVEL 8 - Ovládání pasivního bzučáku rotačním enkodérem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEMES zapojení z Level 6 a nahrazujeme servo bzučákem:
- PONECHÁVÁME: Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN
  - DT k digitálnímu vstupu GP04 (A pin) 
  - CLK k digitálnímu vstupu GP03 (B pin)
  - SW nepoužíváme

- PŘIDÁVÁME: Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

V tomto příkladu se naučíte generovat zvuky pomocí PWM signálu.
Rotačním enkodérem budete plynule měnit frekvenci zvuku.

NOVÉ KONCEPTY:
- Pasivní bzučák a generování tónů
- Frekvence jako výška tónu (Hz)
- PWM s proměnnou frekvencí
- Plynulá změna výšky tónu
- Enkodér pro analogové ovládání

ROZDÍL: Pasivní bzučák potřebuje PWM signál pro generování tónu,
na rozdíl od aktivního bzučáku, který má vlastní generátor.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import rotaryio     # vestavěný modul pro rotační enkodéry
import pwmio        # PWM modul pro generování tónů
import time         # funkce pro čekání a práci s časem

# vytvoření objektu pro enkodér
encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3)

# vytvoření PWM objektu pro bzučák na GP06
# variable_frequency=True umožňuje měnit frekvenci za běhu
buzzer_pwm = pwmio.PWMOut(board.GP6, variable_frequency=True, frequency=440)

# proměnné pro sledování enkodéru a bzučáku
posledni_pozice = 0
frekvence = 440  # počáteční frekvence (A4)

# konstanty pro řízení zvuku
MIN_FREKVENCE = 40    # nejnižší frekvence
MAX_FREKVENCE = 20000  # nejvyšší frekvence (20kHz)
HLASITOST = 2**15      # duty cycle pro hlasitost (50%)

print("Otáčejte enkodérem pro změnu výšky tónu")
print(f"Rozsah: {MIN_FREKVENCE}Hz - {MAX_FREKVENCE}Hz")
print(f"Počáteční frekvence: {frekvence}Hz")
print("Kroky: 20Hz (do 1kHz), 50Hz (1-5kHz), 100Hz (5-10kHz), 200Hz (nad 10kHz)")

# spuštění bzučení na počáteční frekvenci
buzzer_pwm.frequency = frekvence
buzzer_pwm.duty_cycle = HLASITOST

# hlavní smyčka
while True:
    # čtení pozice enkodéru
    aktualni_pozice = encoder.position
    
    # kontrola změny pozice
    if aktualni_pozice != posledni_pozice:
        # výpočet rozdílu
        rozdil = aktualni_pozice - posledni_pozice
        
        # výpočet kroku podle aktuální frekvence (bez funkce)
        if frekvence < 1000:
            krok = 20      # jemné kroky do 1kHz
        elif frekvence < 5000:
            krok = 50      # střední kroky 1-5kHz
        elif frekvence < 10000:
            krok = 100     # větší kroky 5-10kHz
        else:
            krok = 200     # velké kroky nad 10kHz
        
        # změna frekvence podle rozdílu a kroku
        frekvence += rozdil * krok
        
        # omezení frekvence na validní rozsah
        if frekvence < MIN_FREKVENCE:
            frekvence = MIN_FREKVENCE
        elif frekvence > MAX_FREKVENCE:
            frekvence = MAX_FREKVENCE
        
        # nastavení nové frekvence bzučáku
        buzzer_pwm.frequency = frekvence
        
        # výpis pro pochopení
        print(f"Pozice: {aktualni_pozice:4d}, Frekvence: {frekvence:5d}Hz, Krok: {krok:3d}Hz")
        
        # uložení pozice
        posledni_pozice = aktualni_pozice
    
    # krátká pauza
    time.sleep(0.01)
