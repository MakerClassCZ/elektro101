# Level 3 - Ovládání blikání tlačítkem

## Popis
Přidání tlačítka pro ovládání blikání LED. Naučíte se číst digitální vstupy a reagovat na stisk tlačítka.

## Zapojení obvodu
Rozšiřujeme zapojení z Level 2 - ponecháváme obě LED a přidáváme tlačítko:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) první LED veďte odpor 330Ω k zemi (GND)
- Zelenou LED připojte anodou (+) ke GP01  
- Z katody (-) druhé LED veďte odpor 330Ω k zemi (GND)
- **PŘIDÁVÁME:** Tlačítko připojte jedním kontaktem ke GP02
- Druhý kontakt tlačítka připojte k zemi (GND)

## Co se naučíte
- Čtení digitálních vstupů
- Detekci stisku tlačítka
- Pull-up odpory pro stabilní čtení
- Řízení stavu programu pomocí vstupů

## Soubory
- `code.py` - Základní verze s manuálním čtením tlačítka
- `extra-keypad/` - Vylepšená verze s knihovnou `keypad` a neblokujícím časováním
- `extra-async/` - Pokročilá verze s asyncio pro paralelní zpracování úkolů

## Vylepšení
1. **extra-keypad/**: Používá knihovnu `keypad` pro automatický debouncing a event-driven programování
2. **extra-async/**: Asynchronní programování s `asyncio` pro skutečně paralelní běh blikání a čtení tlačítka
