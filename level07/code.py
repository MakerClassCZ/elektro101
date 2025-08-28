"""
LEVEL 7 - Ovládání servo motoru SG90 rotačním enkodérem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 6 a přidáváme servo motor:
- PONECHÁVÁME: Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN
  - DT k digitálnímu vstupu GP04 (A pin) 
  - CLK k digitálnímu vstupu GP03 (B pin)
  - SW nepoužíváme

- PŘIDÁVÁME: Servo motor SG90 připojte:
  - Červený vodič (VCC) k 5V nebo externímu napájení
  - Černý/hnědý vodič (GND) k zemi (GND)
  - Oranžový/žlutý vodič (SIGNAL) k GP05

V tomto příkladu se naučíte ovládat servo motor pomocí PWM signálu.
Rotačním enkodérem budete měnit úhel serva v rozsahu 0° až 180°.

NOVÉ KONCEPTY:
- Servo motor a PWM řízení
- Frekvence 50Hz pro servo signál
- Duty cycle pro úhly serva (1ms-2ms pulzy)
- Mapování pozice enkodéru na úhel serva
- Omezování hodnot na validní rozsah

DŮLEŽITÉ: Servo potřebuje 5V napájení! Pokud nemáte externí zdroj,
můžete zkusit napájení z USB, ale může být nestabilní.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import rotaryio     # vestavěný modul pro rotační enkodéry
import pwmio        # PWM modul pro řízení serva
import time         # funkce pro čekání a práci s časem

# vytvoření objektu pro enkodér pomocí rotaryio
encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3)

# vytvoření PWM objektu pro servo na GP05
# servo potřebuje frekvenci 50Hz (20ms periodu)
servo_pwm = pwmio.PWMOut(board.GP5, frequency=50)

# proměnné pro sledování enkodéru a serva
posledni_pozice = 0
uhel_serva = 90  # střední poloha (0-180°)

# konstanty pro servo řízení
MIN_UHEL = 0      # minimální úhel serva
MAX_UHEL = 180    # maximální úhel serva
KROK_UHLU = 10     # o kolik stupňů se změní úhel při jednom kroku enkodéru

# konstanty pro PWM řízení serva (duty cycle hodnoty)
# servo reaguje na pulzy 1ms-2ms v 20ms periodě
MIN_DUTY = int(65535 * 0.025)  # ~0.5ms (0° pozice) 
MAX_DUTY = int(65535 * 0.125)  # ~2.5ms (180° pozice)

def uhel_na_duty_cycle(uhel):
    """
    Převede úhel serva (0-180°) na odpovídající duty cycle
    """
    # lineární mapování úhlu na duty cycle
    return int(MIN_DUTY + (uhel / MAX_UHEL) * (MAX_DUTY - MIN_DUTY))

# nastavení serva na počáteční pozici
servo_pwm.duty_cycle = uhel_na_duty_cycle(uhel_serva)

print("Otáčejte enkodérem pro ovládání serva")
print(f"Rozsah: {MIN_UHEL}° - {MAX_UHEL}°")
print(f"Aktuální úhel: {uhel_serva}°")

# hlavní smyčka
while True:
    # čtení pozice enkodéru
    aktualni_pozice = encoder.position
    
    # kontrola změny pozice
    if aktualni_pozice != posledni_pozice:
        # výpočet rozdílu (o kolik kroků se pohnul)
        rozdil = aktualni_pozice - posledni_pozice
        
        # změna úhlu podle rozdílu
        uhel_serva += rozdil * KROK_UHLU
        
        # omezení úhlu na validní rozsah
        if uhel_serva < MIN_UHEL:
            uhel_serva = MIN_UHEL
        elif uhel_serva > MAX_UHEL:
            uhel_serva = MAX_UHEL
        
        # převod úhlu na duty cycle a nastavení serva
        duty = uhel_na_duty_cycle(uhel_serva)
        servo_pwm.duty_cycle = duty
        
        # výpis pro pochopení
        print(f"Pozice: {aktualni_pozice:4d}, Změna: {rozdil:+2d}, Úhel: {uhel_serva:3d}°, Duty: {duty:5d}")
        
        # uložení pozice pro příští porovnání
        posledni_pozice = aktualni_pozice
    
    # krátká pauza pro stabilitu
    time.sleep(0.01)
