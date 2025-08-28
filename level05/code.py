"""
LEVEL 5 - Analogové řízení jasu LED potenciometrem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 4 a přidáváme potenciometr:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Potenciometr připojte:
  - Jeden krajní pin k zemi (GND)
  - Druhý krajní pin k ADC_VREF (referenční napětí pro ADC)
  - Střední pin (stěrač) k analogovému vstupu A2

V tomto příkladu se naučíte číst analogové hodnoty z potenciometru
a podle nich řídit jas LED pomocí PWM. Otočením potenciometru
budete měnit jas LED od úplně zhasnuté po plně rozsvícenou.

NOVÉ KONCEPTY:
- Analogové vstupy (analogio.AnalogIn)
- Čtení napětí z potenciometru (0-65535)
- Mapování hodnot z jednoho rozsahu na druhý
- Kombinace analogového vstupu s PWM výstupem
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import analogio     # čtení analogových hodnot
import pwmio        # PWM modul pro řízení jasu
import time         # funkce pro čekání a práci s časem
#import simpleio     # užitečné funkce - map_range, kdyby bylo potřeba mapovat hodnoty na jiný rozsah

# vytvoření objektů
potenciometr = analogio.AnalogIn(board.A2)  # analogový vstup pro potenciometr
led_pwm = pwmio.PWMOut(board.GP0, duty_cycle=0, frequency=1000)  # PWM výstup pro LED

print("Otáčejte potenciometrem pro změnu jasu LED")
print("Hodnoty: potenciometr (0-65535) -> PWM (0-65535)")

# hlavní smyčka
while True:
    # čtení hodnoty z potenciometru (0-65535)
    hodnota_pot = potenciometr.value
    
    # mapování hodnoty potenciometru na PWM duty cycle
    # potenciometr má rozsah 0-65535, PWM také 0-65535, takže můžeme použít přímo
    jas_led = hodnota_pot
    
    # pro jiné rozsahy bychom použili vestavěnou funkci:
    # jas_led = int(simpleio.map_range(hodnota_pot, 0, 65535, 0, 65535))

    # nastavení jasu LED
    led_pwm.duty_cycle = jas_led
    
    # výpis hodnot pro pochopení
    print(f"Potenciometr: {hodnota_pot:5d} -> LED jas: {jas_led:5d}")
    
    # krátká pauza pro čitelnost výstupu
    time.sleep(0.1)
