"""
LEVEL 7 - Ovládání servo motoru SG90 rotačním enkodérem (SERVO KNIHOVNA)

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

Toto je vylepšená verze používající knihovnu adafruit_motor.servo,
která automaticky řeší PWM nastavení a poskytuje jednoduché API.

VYLEPŠENÍ:
- Použití adafruit_motor.servo místo manuálního PWM
- Automatické nastavení duty cycle pro servo
- Jednoduché API s úhly v stupních
- Spolehlivější a přesnější než manuální implementace

Vyžaduje knihovnu adafruit_motor v /lib adresáři.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import rotaryio     # vestavěný modul pro rotační enkodéry
import pwmio        # PWM modul pro řízení serva
import time         # funkce pro čekání a práci s časem
from adafruit_motor import servo  # specializovaná knihovna pro servo motory

# vytvoření objektu pro enkodér pomocí rotaryio
encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3)

# vytvoření PWM objektu pro servo na GP05
servo_pwm = pwmio.PWMOut(board.GP5, frequency=50)

# vytvoření servo objektu pomocí adafruit_motor knihovny
# automaticky nastaví správné duty cycle hodnoty
my_servo = servo.Servo(servo_pwm)

# proměnné pro sledování enkodéru a serva
posledni_pozice = 0
uhel_serva = 90  # střední poloha (0-180°)

# konstanty pro servo řízení
MIN_UHEL = 0      # minimální úhel serva
MAX_UHEL = 180    # maximální úhel serva
KROK_UHLU = 5     # o kolik stupňů se změní úhel při jednom kroku enkodéru

# nastavení serva na počáteční pozici
my_servo.angle = uhel_serva

print("Otáčejte enkodérem pro ovládání serva")
print(f"Rozsah: {MIN_UHEL}° - {MAX_UHEL}°")
print(f"Aktuální úhel: {uhel_serva}°")
print("Používáme adafruit_motor.servo knihovnu")

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
        
        # nastavení úhlu serva (jednoduché API!)
        my_servo.angle = uhel_serva
        
        # výpis pro pochopení
        print(f"Pozice: {aktualni_pozice:4d}, Změna: {rozdil:+2d}, Úhel serva: {uhel_serva:3d}°")
        
        # uložení pozice pro příští porovnání
        posledni_pozice = aktualni_pozice
    
    # krátká pauza pro stabilitu
    time.sleep(0.01)
