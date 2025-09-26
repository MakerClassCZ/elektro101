# Level 12 - OLED Display s teplotním senzorem SHT40

## Popis
Kombinace I2C senzoru s OLED displejem pro zobrazení dat. Naučíte se pracovat s více zařízeními na jedné I2C sběrnici.

## Zapojení obvodu
Na I2C sběrnici připojíme dva moduly:

1) **SHT40 senzor teploty a vlhkosti:**
   - VDD k 3V3
   - GND k zemi (GND)
   - SDA k GP16 (I2C data - modrá)
   - SCL k GP17 (I2C clock - žlutá)

2) **OLED Display SSD1306 128x64:**
   - Připojený na sběrnici pomocí uŠup

## Co se naučíte
- OLED display SSD1306 (128x64 pixelů)
- Více zařízení na jedné I2C sběrnici
- Textové zobrazení na displeji
- Knihovna `displayio` pro grafiku
- Kombinace senzoru a displeje

## Soubory
- `code.py` - Zobrazení teploty a vlhkosti na OLED displeji
- `scan.py` - I2C scanner pro detekci připojených zařízení

## Pomůcky
**scan.py**: I2C scanner, který:
- Projde všechny možné I2C adresy (0x08-0x77)
- Detekuje připojená zařízení
- Rozpozná známé senzory podle jejich adres
- Pomáhá při diagnostice problémů s I2C komunikací
