import board
import time
import digitalio
import rotaryio
import usb_hid
import neopixel
import busio
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import terminalio
from adafruit_hid import Keyboard
from adafruit_hid import Keycode
from adafruit_hid import ConsumerControl
from adafruit_hid import ConsumerControlCode


keyboard = Keyboard(usb_hid.devices)
consumer_control = ConsumerControl(usb_hid.devices)

displayio.release_displays()
i2c = busio.I2C(scl=board.SCL, sda=board.SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

text_display = False

def show_cat():
    splash = displayio.Group()
    display.show(splash)
    txt = label.Label(terminalio.FONT, text=" (^._.^)~ Cat ", color=0xFFFFFF, x=15, y=28)
    splash.append(txt)

def show_text():
    splash = displayio.Group()
    display.show(splash)
    txt = label.Label(terminalio.FONT, text="You can do it", color=0x00FFFF, x=128, y=32)
    splash.append(txt)
    for i in range(128, -100, -1):
        txt.x = i
        time.sleep(0.02)

leds = neopixel.NeoPixel(board.D1, 4, brightness=0.2, auto_write=False)

def fade_leds():
    for b in range(0, 255, 5):
        leds.fill((0, 0, b))
        leds.show()
        time.sleep(0.01)
    for b in range(255, 0, -5):
        leds.fill((0, 0, b))
        leds.show()
        time.sleep(0.01)

encoder = rotaryio.IncrementalEncoder(board.D2, board.D3)
encoder_button = digitalio.DigitalInOut(board.D4)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP
last_position = encoder.position

key_pins = [board.D5, board.D6, board.D7, board.D8, board.D9, board.D10, board.D11, board.D12, board.D13]
keys = []
for pin in key_pins:
    k = digitalio.DigitalInOut(pin)
    k.direction = digitalio.Direction.INPUT
    k.pull = digitalio.Pull.UP
    keys.append(k)

def press_hotkey(keys):
    for k in keys:
        keyboard.press(k)
    keyboard.release_all()

def open_app(cmd):
    keyboard.press(Keycode.WINDOWS, Keycode.R)
    keyboard.release_all()
    time.sleep(0.5)
    for c in cmd:
        keyboard.press(getattr(Keycode, c.upper()) if hasattr(Keycode, c.upper()) else c)
        keyboard.release_all()
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()

show_cat()

while True:
    pos = encoder.position
    if pos != last_position:
        diff = pos - last_position
        last_position = pos
        if diff > 0:
            consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
        else:
            consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)

    fade_leds()

    for i, k in enumerate(keys):
        if not k.value:
            time.sleep(0.2)
            if i == 0:
                open_app("opera https://youtube.com")
            elif i == 1:
                open_app("opera https://github.com")
            elif i == 2:
                open_app("code")
            elif i == 3:
                open_app("figma")
            elif i == 4:
                keyboard.send(Keycode.CONTROL, Keycode.C)
            elif i == 5:
                keyboard.send(Keycode.CONTROL, Keycode.V)
            elif i == 6:
                open_app("whatsapp")
            elif i == 7:
                open_app("opera")
            elif i == 8:
                text_display = not text_display
                if text_display:
                    show_text()
                else:
                    show_cat()

    time.sleep(0.01)
