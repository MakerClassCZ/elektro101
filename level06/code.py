"""
LEVEL 6 - Řízení jasu LED rotačním enkodérem

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 4 a nahrazujeme potenciometr enkodérem:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN (NUTNÉ pro tento modul!)
  - DT k digitálnímu vstupu GP03 (A pin)
  - CLK k digitálnímu vstupu GP04 (B pin)  
  - SW nepoužíváme (lze připojit později)

DŮLEŽITÉ: Pin + u tohoto modulu MUSÍ být zapojen, jinak enkodér nefunguje!

V tomto příkladu se naučíte číst rotační enkodér a podle jeho otáčení
zvyšovat nebo snižovat jas LED. Enkodér poskytuje nekonečné otáčení
s přesným zaznamenáváním směru.

NOVÉ KONCEPTY:
- Rotační enkodér (quadrature encoder)
- Čtení dvou digitálních signálů současně
- Detekce směru otáčení pomocí fázového rozdílu
- Akumulace pozice enkodéru
- Omezování hodnot na daný rozsah
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import digitalio    # práce s digitálními vstupy a výstupy
import pwmio        # PWM modul pro řízení jasu
import time         # funkce pro čekání a práci s časem

# vytvoření objektů
led_pwm = pwmio.PWMOut(board.GP0, duty_cycle=0, frequency=1000)  # PWM výstup pro LED

# vytvoření objektů pro enkodér
dt_pin = digitalio.DigitalInOut(board.GP3)  # DT pin (A kanál)
dt_pin.direction = digitalio.Direction.INPUT
dt_pin.pull = digitalio.Pull.UP

clk_pin = digitalio.DigitalInOut(board.GP4)  # CLK pin (B kanál)
clk_pin.direction = digitalio.Direction.INPUT
clk_pin.pull = digitalio.Pull.UP

# proměnné pro sledování enkodéru
posledni_clk = clk_pin.value
pozice_enkoderu = 0  # aktuální pozice enkodéru
jas_led = 0  # aktuální jas LED (0-65535)

# konstanta pro citlivost enkodéru
KROK_JASU = 2000  # o kolik se změní jas při jednom kroku enkodéru

print("Otáčejte enkodérem pro změnu jasu LED")
print("Vlevo = tmavší, Vpravo = světlejší")

# hlavní smyčka
while True:
    # čtení aktuálního stavu CLK pinu
    aktualni_clk = clk_pin.value
    
    # detekce změny (hrany)
    if aktualni_clk != posledni_clk:
        # změna nastala - zkontrolujeme směr
        if aktualni_clk == dt_pin.value:
            # CLK a DT jsou stejné = otáčení vlevo (counter-clockwise)
            pozice_enkoderu -= 1
            jas_led -= KROK_JASU
        else:
            # CLK a DT jsou různé = otáčení vpravo (clockwise)
            pozice_enkoderu += 1
            jas_led += KROK_JASU
        
        # omezení jasu na rozsah 0-65535
        if jas_led < 0:
            jas_led = 0
        elif jas_led > 65535:
            jas_led = 65535
        
        # nastavení jasu LED
        led_pwm.duty_cycle = jas_led
        
        # výpis pro pochopení
        print(f"Pozice: {pozice_enkoderu:4d}, Jas LED: {jas_led:5d}")
        
        # uložení stavu pro příští porovnání
        posledni_clk = aktualni_clk
    
    # krátká pauza pro stabilitu
    time.sleep(0.001)
