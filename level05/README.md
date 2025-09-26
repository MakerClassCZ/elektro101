# Level 5 - Analogové řízení jasu LED potenciometrem

## Popis
Kombinace analogového vstupu s PWM výstupem. Naučíte se číst hodnoty z potenciometru a podle nich řídit jas LED.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 4 a přidáváme potenciometr:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)
- **PŘIDÁVÁME:** Potenciometr připojte:
  - Jeden krajní pin k zemi (GND)
  - Druhý krajní pin k ADC_VREF (referenční napětí pro ADC)
  - Střední pin (stěrač) k analogovému vstupu A2

## Co se naučíte
- Analogové vstupy (`analogio.AnalogIn`)
- Čtení napětí z potenciometru (0-65535)
- Mapování hodnot z jednoho rozsahu na druhý
- Kombinaci analogového vstupu s PWM výstupem

## Soubory
- `code.py` - Ovládání jasu LED otáčením potenciometru
