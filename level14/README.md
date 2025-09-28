# Level 14 - NeoPixel Matrix 4x4

## Popis
Úvod do adresovatelných RGB LED. Naučíte se vytvářet různé vzory, animace a efekty.

## Zapojení obvodu
NeoPixel matrix 4x4 připojte:
- VCC k 3V3 nebo 5V
- GND k zemi (GND)
- DIN (Data Input) k GP18

**POZNÁMKA:** NeoPixel matrix může potřebovat externí napájení při plném jasu. Pro testování a nižší jas by mělo stačit napájení z Pico nebo 5V z USB.

## Co se naučíte
- Adresovatelné RGB LED (NeoPixel/WS2812)
- Matrix indexování (2D -> 1D mapování)
- Barevné prostory (RGB, HSV)
- Animace a efekty
- Různé vzory a jejich implementace

## Soubory
- `code.py` - Základní postupné rozsvěcování LED s různými barvami
- `code-demo.py` - Pokročilé vzory a animace (kříž, rohy, rámeček, diagonála, šachovnice, duha)
- `code-interactive.py` - Interaktivní ovládání tlačítkem pro přepínání vzorů
- `code-encoder.py` - Ovládání enkodérem pro plynulé změny jasu, barvy a vzorů

## Vylepšení
1. **code-demo.py**: Pokročilé vzory a animace včetně duhového cyklu a breathing efektu
2. **code-interactive.py**: Interaktivní ovládání tlačítkem s cyklickým přepínáním vzorů
3. **code-encoder.py**: Kompletní ovládání enkodérem s HSV barevným prostorem a různými módy
