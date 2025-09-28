# Level 8 - Ovládání pasivního bzučáku rotačním enkodérem

## Popis
Nahrazení servo motoru pasivním bzučákem pro generování zvuků. Naučíte se vytvářet tóny pomocí PWM signálu.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 6 a nahrazujeme servo bzučákem:
- **PONECHÁVÁME:** Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN
  - DT k digitálnímu vstupu GP04 (A pin) 
  - CLK k digitálnímu vstupu GP03 (B pin)
  - SW nepoužíváme

- **PŘIDÁVÁME:** Pasivní bzučák připojte:
  - Kladný pin k GP06 (PWM výstup)
  - Záporný pin k zemi (GND)

## Co se naučíte
- Pasivní bzučák a generování tónů
- Frekvence jako výška tónu (Hz)
- PWM s proměnnou frekvencí
- Plynulá změna výšky tónu
- Enkodér pro analogové ovládání

**ROZDÍL:** Pasivní bzučák potřebuje PWM signál pro generování tónu, na rozdíl od aktivního bzučáku, který má vlastní generátor.

## Soubory
- `code.py` - Základní ovládání frekvence enkodérem
- `extra-melodie/` - Vylepšená verze s přehráváním melodií

## Vylepšení
**extra-melodie/**: Používá `simpleio.tone()` pro přehrávání tónů a poskytuje:
- Předefinované melodie (Twinkle Twinkle, Happy Birthday, atd.)
- Enkodér pro výběr melodie
- Tlačítko pro spuštění vybrané melodie
- LED indikátor při přehrávání melodie
- Jednodušší API než manuální PWM
