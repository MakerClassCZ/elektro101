"""
MACROPAD FULL - Programovatelná klávesnice s makry, enkodérem a NeoPixel

ZAPOJENÍ DESKY:

1) Tlačítka (6x):
   - Tlačítko 0: GP19 → LEFT_ARROW (červená)
   - Tlačítko 1: GP21 → RIGHT_ARROW (zelená)
   - Tlačítko 2: GP27 → ENTER (modrá)
   - Tlačítko 3: GP20 → MUTE MIKE (žlutá)
   - Tlačítko 4: GP22 → MACRO 1 (fialová)
   - Tlačítko 5: GP26 → MACRO 2 (tyrkysová)

2) Rotační enkodér:
   - A: GP16 → zvýšení hlasitosti
   - B: GP17 → snížení hlasitosti
   - SW: GP15 → MUTE (bílá)

3) NeoPixel LED:
   - DIN: GP11 → indikace stisknutých tlačítek

4) I2C konektor (volitelně):
   - SDA: GP12
   - SCL: GP13

JAK FUNGUJE:
Programovatelná klávesnice s USB HID emulací, rotačním enkodérem pro hlasitost
a NeoPixel indikací. Každé tlačítko má svou barvu a při stisknutí krátce blikne.
Enkodér ovládá hlasitost a jeho stisknutí ztlumí/zapne zvuk.
"""

import time
import board
import keypad
import usb_hid
import rotaryio
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from keyboard_layout_win_cz import KeyboardLayout

# nastavení klávesnice a rozložení
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)
cc = ConsumerControl(usb_hid.devices) # kódy pro ovládání multimédií

# definice tlačítek (6 hlavních + 1 tlačítko enkodéru)
buttons = keypad.Keys(
    pins=[board.GP19, board.GP21, board.GP27, board.GP20, board.GP22, board.GP26, board.GP15],
    value_when_pressed=False
)

# rotační enkodér
encoder = rotaryio.IncrementalEncoder(board.GP16, board.GP17)

# NeoPixel LED
pixel = neopixel.NeoPixel(board.GP11, 1, brightness=0.3, auto_write=True)

# barvy pro jednotlivá tlačítka (6 hlavních + 1 tlačítko enkodéru)
BUTTON_COLORS = [
    (255, 0, 0),    # 0 - červená (LEFT)
    (0, 255, 0),    # 1 - zelená (RIGHT)
    (0, 0, 255),    # 2 - modrá (ENTER)
    (255, 255, 0),  # 3 - žlutá (MUTE MIKE)
    (255, 0, 255),  # 4 - fialová (MACRO 1)
    (0, 255, 255),  # 5 - tyrkysová (MACRO 2)
    (255, 255, 255), # 6 - bílá (MUTE - tlačítko enkodéru)
]

# stav enkodéru
last_position = encoder.position

# stav NeoPixelu - časovač, do kdy má být pixel rozsvícený (pokud > 0, pixel svítí do tohoto času, pak se zhasne)
pixel_timer = 0  # čas se počítá pomocí time.monotonic() - absolutní čas od startu (sekundy)

# globální proměnná pro události
event = keypad.Event()

# Žádné funkce - inline kód pro maximální rychlost

print("🎹 MACROPAD FULL spuštěn!")
print("Tlačítka: LEFT, RIGHT, ENTER, MUTE MIKE, MACRO 1, MACRO 2, MUTE (enkodér)")
print("Enkodér: otáčení = hlasitost, stisknutí = MUTE")
print("NeoPixel: indikace stisknutých tlačítek")

while True:
    # zpracování tlačítek
    if buttons.events.get_into(event):
        if event.pressed:
            # rozsvítí NeoPixel barvou odpovídající tlačítku
            if 0 <= event.key_number < len(BUTTON_COLORS):
                pixel.fill(BUTTON_COLORS[event.key_number])
                pixel_timer = time.monotonic() + 0.3 # timer na další 0.3 sekundy
            
            # akce podle stisknutého tlačítka
            if event.key_number == 0:
                kbd.send(Keycode.LEFT_ARROW)
                print("LEFT")
            elif event.key_number == 1:
                kbd.send(Keycode.RIGHT_ARROW)
                print("RIGHT")
            elif event.key_number == 2:
                kbd.send(Keycode.ENTER)
                print("ENTER")
            elif event.key_number == 3:
                # Zoom & Teams: Ctrl+Shift+M
                # kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.M)
                # Google Meet: Ctrl+D
                kbd.send(Keycode.CONTROL, Keycode.D)
                print("MUTE MIKE")
            elif event.key_number == 4:
                # MACRO 1: Win+R, notepad
                kbd.send(Keycode.GUI, Keycode.R)
                time.sleep(0.2)
                layout.write("notepad")
                time.sleep(0.2)
                kbd.send(Keycode.ENTER)
                time.sleep(0.2)
                layout.write("Ahoj z MakerClass!")
                print("MACRO 1")
            elif event.key_number == 5:
                # MACRO 2: Alt+Tab
                kbd.press(Keycode.ALT, Keycode.TAB)  # ALT+TAB - všimni si, že je použit press a release, nikoli send
                time.sleep(0.2)
                kbd.release(Keycode.TAB) # uvolní TAB, ale stále drží ALT
                time.sleep(0.2)
                kbd.send(Keycode.TAB)  # Stiskne TAB znovu, zatímco stále drží ALT
                time.sleep(0.2)
                kbd.release_all()
                print("MACRO 2")
            elif event.key_number == 6:
                # MUTE (tlačítko enkodéru)
                cc.send(ConsumerControlCode.MUTE)
                print("MUTE (enkodér)")
    


    # zpracování rotačního enkodéru
    current_position = encoder.position
    if current_position != last_position:
        if current_position > last_position:
            # otáčení doprava - zvýšení hlasitosti
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            pixel.fill((0, 255, 100))
            pixel_timer = time.monotonic() + 0.1
            print("Hlasitost +")
        else:
            # otáčení doleva - snížení hlasitosti
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            pixel.fill((255, 100, 0))
            pixel_timer = time.monotonic() + 0.1
            print("Hlasitost -")
        last_position = current_position
    


    # aktualizace NeoPixel timeru
    if pixel_timer > 0 and time.monotonic() >= pixel_timer:
        pixel.fill((0, 0, 0))
        pixel_timer = 0
    
