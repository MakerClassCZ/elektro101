# Level 6 - Řízení jasu LED rotačním enkodérem

## Popis
Nahrazení potenciometru rotačním enkodérem pro přesnější ovládání. Naučíte se pracovat s enkodérem a detekovat směr otáčení.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 4 a nahrazujeme potenciometr enkodérem:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) LED veďte odpor 330Ω k zemi (GND)
- **PŘIDÁVÁME:** Rotační enkodér připojte:
  - GND k zemi (GND)
  - + k ADC_VREF nebo 3V3_EN (NUTNÉ pro tento modul!)
  - DT k digitálnímu vstupu GP03 (A pin)
  - CLK k digitálnímu vstupu GP04 (B pin)  
  - SW nepoužíváme (lze připojit později)

**DŮLEŽITÉ:** Pin + u tohoto modulu MUSÍ být zapojen, jinak enkodér nefunguje!

## Co se naučíte
- Rotační enkodér (quadrature encoder)
- Čtení dvou digitálních signálů současně
- Detekci směru otáčení pomocí fázového rozdílu
- Akumulaci pozice enkodéru
- Omezování hodnot na daný rozsah

## Soubory
- `code.py` - Manuální implementace čtení enkodéru
- `extra-rotaryio/` - Vylepšená verze s vestavěným modulem `rotaryio`

## Vylepšení
**extra-rotaryio/**: Používá `rotaryio.IncrementalEncoder` místo manuálního čtení, což poskytuje:
- Automatickou detekci směru a počítání kroků
- Spolehlivější a přesnější než manuální implementace
- Méně kódu, více funkcí
