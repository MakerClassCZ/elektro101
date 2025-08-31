"""
MACROPAD - Programovatelná klávesnice s makry

ZAPOJENÍ DESKY:

1) Tlačítka (6x):
   - Tlačítko 0: GP19
   - Tlačítko 1: GP21
   - Tlačítko 2: GP27
   - Tlačítko 3: GP20
   - Tlačítko 4: GP22
   - Tlačítko 5: GP26

2) Rotační enkodér (volitelně):
   - A: GP16
   - B: GP17
   - SW: GP15 (stisknutí enkodéru)

3) NeoPixel LED (volitelně):
   - DIN: GP11

4) I2C konektor (volitelně):
   - SDA: GP12
   - SCL: GP13

JAK FUNGUJE:
Programovatelná klávesnice, která emuluje USB HID zařízení.
Každé tlačítko může odeslat libovolnou kombinaci kláves nebo spustit makro.
"""

import time
import board
import keypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
# výchozí US rozložení klávesnice
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
# rozložení klávesnice najdete zde: https://github.com/Neradoc/Circuitpython_Keyboard_Layouts
# zde použijeme české rozložení klávesnice
from keyboard_layout_win_cz import KeyboardLayout

# nastavení klávesnice a rozložení
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

# definice tlačítek
buttons = keypad.Keys(
    pins=[board.GP19, board.GP21, board.GP27, board.GP20, board.GP22, board.GP26],
    value_when_pressed = False
)

# globální proměnná pro události - bude ukládat, které tlačítko bylo stisknuto
event = keypad.Event()

while True:
    if buttons.events.get_into(event):
        if event.pressed:
            # předdefinované kódy kláves najdete zde: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keycode.py    
            # nebo v oficiální dokumentaci - kapitola 10 https://usb.org/sites/default/files/hut1_21.pdf        
            if event.key_number == 0:
                kbd.send(Keycode.LEFT_ARROW)
                print("LEFT")
            elif event.key_number == 1:
                kbd.send(Keycode.RIGHT_ARROW)
                print("RIGHT")
            elif event.key_number == 2: # Klávesa Enter, ale odeslána numerickým kódem 0x28 (jen pro příklad)
                kbd.send(0x28)
                print("ENTER")
            elif event.key_number == 3:  # Ztlumení mikrofonu v Zoom, Teams nebo Google Meet, vyberte který používáte
                # Zoom & Teams: Ctrl+Shift+M
                # kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.M)
                # Google Meet: Ctrl+D
                kbd.send(Keycode.CONTROL, Keycode.D)
                print("MUTE")
            elif event.key_number == 4:  # Příklad složitého makra
                kbd.send(Keycode.GUI, Keycode.R)
                time.sleep(0.2)
                layout.write("notepad") # převádí řetězec na kódy kláves a odesílá je, musíte použít správné rozložení klávesnice
                time.sleep(0.2)
                kbd.send(Keycode.ENTER)
                time.sleep(0.2)
                layout.write("Ahoj z MakerClass!")
                print("MACRO 1")
            elif event.key_number == 5:  # Další okno - příklad stisknutí, držení a uvolnění klávesy
                kbd.press(Keycode.ALT, Keycode.TAB)  # ALT+TAB
                time.sleep(0.2)
                kbd.release(Keycode.TAB) # uvolní TAB, ale stále drží ALT
                time.sleep(0.2)
                kbd.send(Keycode.TAB)  # Stiskne TAB znovu, zatímco stále drží ALT
                time.sleep(0.2)
                kbd.release_all()  # Uvolní všechny klávesy
                print("MACRO 2")