"""
LEVEL 3 - Ovládání blikání tlačítkem (ASYNC ŘEŠENÍ)

ZAPOJENÍ OBVODU:
ROZŠIŘUJEME zapojení z Level 2 - ponecháváme obě LED a přidáváme tlačítko:
- Červenou LED připojte anodou (+) ke GP00
- Z katody (-) první LED veďte odpor 330Ω k zemi (GND)
- Zelenou LED připojte anodou (+) ke GP01  
- Z katody (-) druhé LED veďte odpor 330Ω k zemi (GND)
- PŘIDÁVÁME: Tlačítko připojte jedním kontaktem ke GP02
- Druhý kontakt tlačítka připojte k zemi (GND)

Toto je nejpokročilejší verze používající asyncio pro skutečně paralelní 
zpracování úkolů. Blikání LED a čtení tlačítka běží jako samostatné úkoly.

POKROČILÉ KONCEPTY:
- Asynchronní programování s asyncio
- Paralelní běh více úkolů současně
- Sdílení stavu mezi úkoly
- Neblokující operace

Vyžaduje knihovnu asyncio v /lib adresáři.
"""

# import knihoven pro práci s hardware
import board        # přístup k pinům a hardware zařízení
import digitalio    # práce s digitálními vstupy a výstupy
import asyncio      # asynchronní programování
import keypad       # pokročilá práce s tlačítky a událostmi

# vytvoření objektů pro LED
led1 = digitalio.DigitalInOut(board.GP0)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP1)
led2.direction = digitalio.Direction.OUTPUT

# vytvoření keypad objektu pro tlačítko
keys = keypad.Keys((board.GP2,), value_when_pressed=False, pull=True)

# globální stav sdílený mezi úkoly
blikani_zapnuto = False

# asynchronní úkol pro blikání LED
async def blink_leds():
    """Úkol pro střídání LED s nastavenou rychlostí"""
    while True:
        if blikani_zapnuto:
            # rozsvícení červené, zhasnutí zelené
            led1.value = True
            led2.value = False
            await asyncio.sleep(0.5)
            
            # zhasnutí červené, rozsvícení zelené
            led1.value = False
            led2.value = True
            await asyncio.sleep(0.5)
        else:
            # vypnutí obou LED
            led1.value = False
            led2.value = False
            await asyncio.sleep(0.1)  # krátká pauza při vypnutém blikání

# asynchronní úkol pro čtení tlačítka
async def button_handler():
    """Úkol pro zpracování událostí tlačítka"""
    global blikani_zapnuto
    
    while True:
        # kontrola událostí tlačítka
        event = keys.events.get()
        
        if event and event.pressed:
            # přepnutí stavu blikání
            blikani_zapnuto = not blikani_zapnuto
            print(f"Blikání: {'ZAPNUTO' if blikani_zapnuto else 'VYPNUTO'}")
        
        # velmi krátká pauza pro efektivitu
        await asyncio.sleep(0)

# hlavní asynchronní funkce
async def main():
    """Spuštění všech úkolů paralelně"""
    print("Program spuštěn. Stiskněte tlačítko pro zapnutí/vypnutí blikání")
    
    # spuštění obou úkolů současně
    await asyncio.gather(
        blink_leds(),
        button_handler()
    )

# spuštění event loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program ukončen")
