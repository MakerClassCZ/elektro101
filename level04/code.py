"""
LEVEL 4 - PWM řídicí jas LED

ZAPOJENÍ OBVODU:
Používáme stejné zapojení jako v Level 1, ale využijeme pouze první LED:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)

V tomto příkladu se naučíte používat PWM (Pulse Width Modulation) pro řízení 
jasu LED. PWM rychle zapíná a vypíná LED s různým poměrem zapnutí/vypnutí,
což vytváří dojem různého jasu.

NOVÉ KONCEPTY:
- PWM (Pulse Width Modulation) - modulace šířky pulzu
- duty_cycle - poměr zapnutí/vypnutí (0-65535)
- Postupné zesilování a zeslabování (breathing effect)
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import pwmio        # PWM modul pro řízení jasu
import time         # funkce pro čekání a práci s časem

# vytvoření PWM objektu pro LED na GP00
# duty_cycle=0 znamená LED vypnuta, 65535 znamená plně rozsvícena
led_pwm = pwmio.PWMOut(board.GP0, duty_cycle=0, frequency=1000)

# konstanta pro rychlost změny jasu
KROK = 512  # o kolik se změní jas v každém kroku
PAUZA = 0.02  # jak dlouho čekat mezi kroky (sekundy)

print("Spuštěn PWM efekt breathing - postupné zesilování a zeslabování LED")

# hlavní smyčka pro breathing efekt
while True:
    # postupné zesilování LED (od 0 do maximum)
    for jas in range(0, 65536, KROK):
        led_pwm.duty_cycle = jas
        time.sleep(PAUZA)
    
    # postupné zeslabování LED (od maxima do 0)
    for jas in range(65535, -1, -KROK):
        led_pwm.duty_cycle = jas
        time.sleep(PAUZA)
