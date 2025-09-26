# Level 15 - NeoPixel Matrix + Akcelerometr - Kulička na náklonu

## Popis
Kombinace všech předchozích znalostí do interaktivní hry. Naučíte se spojit senzory s výstupem a vytvořit herní aplikaci s fyzikou.

## Zapojení obvodu
Kombinujeme hardware z Level 13 a Level 14:

1) **NeoPixel matrix 4x4:**
   - VCC k 3V3 nebo 5V
   - GND k zemi (GND)
   - DIN k GP18

2) **MPU6500/MPU6050 akcelerometr (I2C):**
   - VCC k 3V3
   - GND k zemi (GND)
   - SDA k GP16 (I2C data - modrá)
   - SCL k GP17 (I2C clock - žlutá)

3) **Pasivní bzučák (pro pípání při nárazu):**
   - Kladný pin k GP06
   - Záporný pin k zemi (GND)

## Co se naučíte
- Spojení senzoru s výstupem (input → processing → output)
- Herní smyčka (game loop)
- Základní fyzika (pozice, rychlost, zrychlení)
- Mapování hodnot senzoru na herní svět
- Interaktivní zpětná vazba
- Zvuková indikace událostí

## Herní mechanika
- Kulička (červená LED) se pohybuje podle náklonu Pico
- Nakloníte-li Pico doprava → kulička se valí doprava
- Nakloníte-li Pico doleva → kulička se valí doleva
- Kulička se zastaví na okrajích matice
- Při nárazu na stěnu se přehraje krátké pípnutí

## Soubory
- `code.py` - Kompletní hra s fyzikou, zvukovou zpětnou vazbou a debug informacemi
