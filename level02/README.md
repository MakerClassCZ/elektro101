# Level 2 - Střídání dvou LED diod

## Popis
Rozšíření předchozího levelu o druhou LED diodu. Naučíte se pracovat s více výstupy současně a koordinovat jejich chování.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 1 - ponecháváme první LED a přidáváme druhou:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) první LED veďte odpor 330Ω k zemi (GND)
- **PŘIDÁVÁME:** Druhou LED připojte anodou (+) ke GP01  
- Z katody (-) druhé LED veďte odpor 330Ω k zemi (GND)

## Co se naučíte
- Práci s více GPIO výstupy současně
- Koordinaci chování více LED
- Střídání stavů LED (když jedna svítí, druhá je zhasnutá)

## Soubory
- `code.py` - Střídání dvou LED s půlsekundovými intervaly
