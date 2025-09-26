# Level 7 - Ovládání servo motoru SG90 rotačním enkodérem

## Popis
Přidání servo motoru pro mechanické ovládání. Naučíte se generovat PWM signály pro servo motory a řídit jejich úhel.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 6 a přidáváme servo motor:
- **PONECHÁVÁME:** Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN
  - DT k digitálnímu vstupu GP04 (A pin) 
  - CLK k digitálnímu vstupu GP03 (B pin)
  - SW nepoužíváme

- **PŘIDÁVÁME:** Servo motor SG90 připojte:
  - Červený vodič (VCC) k 5V nebo externímu napájení
  - Černý/hnědý vodič (GND) k zemi (GND)
  - Oranžový/žlutý vodič (SIGNAL) k GP05

## Co se naučíte
- Servo motor a PWM řízení
- Frekvence 50Hz pro servo signál
- Duty cycle pro úhly serva (1ms-2ms pulzy)
- Mapování pozice enkodéru na úhel serva
- Omezování hodnot na validní rozsah

**DŮLEŽITÉ:** Servo potřebuje 5V napájení! Pokud nemáte externí zdroj, můžete zkusit napájení z USB, ale může být nestabilní.

## Soubory
- `code.py` - Manuální implementace PWM pro servo s enkodérem
- `code-servo.py` - Vylepšená verze s knihovnou `adafruit_motor.servo` a enkodérem
- `code-input.py` - Ovládání ze sériové konzole bez enkodéru

## Vylepšení
1. **code-servo.py**: Používá `adafruit_motor.servo` místo manuálního PWM, což poskytuje:
   - Automatické nastavení duty cycle pro servo
   - Jednoduché API s úhly v stupních
   - Spolehlivější a přesnější než manuální implementace

2. **code-input.py**: Interaktivní ovládání ze sériové konzole s:
   - Čtením číselného vstupu ze sériové konzole
   - Validací uživatelského vstupu (0-180°)
   - Použitím jednoduché knihovny `simpleio` pro servo ovládání


