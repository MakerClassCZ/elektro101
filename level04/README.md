# Level 4 - PWM řízení jasu LED

## Popis
Úvod do PWM (Pulse Width Modulation) pro plynulé řízení jasu LED. Naučíte se vytvářet "breathing" efekt.

## Zapojení obvodu
Používáme stejné zapojení jako v Level 1, ale využijeme pouze první LED:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)

## Co se naučíte
- PWM (Pulse Width Modulation) - modulace šířky pulzu
- `duty_cycle` - poměr zapnutí/vypnutí (0-65535)
- Postupné zesilování a zeslabování (breathing effect)
- Práci s `pwmio` knihovnou

## Soubory
- `code.py` - Breathing efekt s postupným zesilováním a zeslabováním LED
