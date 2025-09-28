"""
LEVEL 6 - Řízení jasu LED rotačním enkodérem (ROTARYIO VERZE)

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 4 a nahrazujeme potenciometr enkodérem:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN (NUTNÉ pro tento modul!)
  - DT k digitálnímu vstupu GP04 (A pin) 
  - CLK k digitálnímu vstupu GP03 (B pin)
  NEBO prohod zapojení DT/CLK pokud se enkodér otáčí opačně  
  - SW nepoužíváme (lze připojit později)

Toto je vylepšená verze používající vestavěný modul rotaryio, který 
poskytuje jednodušší a spolehlivější práci s enkodérem.

VYLEPŠENÍ:
- Použití rotaryio.IncrementalEncoder místo manuálního čtení
- Automatická detekce směru a počítání kroků
- Spolehlivější a přesnější než manuální implementace
- Méně kódu, více funkcí
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import rotaryio     # vestavěný modul pro rotační enkodéry
import pwmio        # PWM modul pro řízení jasu
import time         # funkce pro čekání a práci s časem

# vytvoření objektů
led_pwm = pwmio.PWMOut(board.GP0, duty_cycle=0, frequency=1000)  # PWM výstup pro LED

# vytvoření objektu pro enkodér pomocí rotaryio
# pokud se enkodér otáčí opačně, prohod piny GP3 a GP4
encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3)

# proměnné pro sledování enkodéru
posledni_pozice = 0
jas_led = 0  # aktuální jas LED (0-65535)

# konstanta pro citlivost enkodéru
KROK_JASU = 2000  # o kolik se změní jas při jednom kroku enkodéru

print("Otáčejte enkodérem pro změnu jasu LED")
print("Vlevo = tmavší, Vpravo = světlejší")
print("Používáme rotaryio.IncrementalEncoder")

# hlavní smyčka
while True:
    # čtení pozice enkodéru (automaticky se počítá)
    aktualni_pozice = encoder.position
    
    # kontrola změny pozice
    if aktualni_pozice != posledni_pozice:
        # výpočet rozdílu (o kolik kroků se pohnul)
        rozdil = aktualni_pozice - posledni_pozice
        
        # změna jasu podle rozdílu
        jas_led += rozdil * KROK_JASU
        
        # omezení jasu na rozsah 0-65535
        if jas_led < 0:
            jas_led = 0
        elif jas_led > 65535:
            jas_led = 65535
        
        # nastavení jasu LED
        led_pwm.duty_cycle = jas_led
        
        # výpis pro pochopení
        print(f"Pozice: {aktualni_pozice:4d}, Změna: {rozdil:+2d}, Jas LED: {jas_led:5d}")
        
        # uložení pozice pro příští porovnání
        posledni_pozice = aktualni_pozice
    
    # krátká pauza pro stabilitu
    time.sleep(0.01)
