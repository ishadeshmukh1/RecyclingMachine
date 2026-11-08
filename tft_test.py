from PIL import Image, ImageDraw, ImageFont
import spidev
import time
from gpiozero import DigitalOutputDevice

# -----------------------------
# GPIO PINS
# -----------------------------
DC = 24
RST = 25
CS = 8

# -----------------------------
# DISPLAY SETTINGS
# -----------------------------
WIDTH = 240
HEIGHT = 320

# -----------------------------
# GPIO SETUP
# -----------------------------
dc = DigitalOutputDevice(DC)
rst = DigitalOutputDevice(RST)

# -----------------------------
# SPI SETUP
# -----------------------------
spi = spidev.SpiDev()
spi.open(0, 0)   # Bus 0, CE0
spi.max_speed_hz = 32000000
spi.mode = 0

# -----------------------------
# LOW LEVEL FUNCTIONS
# -----------------------------
def command(cmd):
    dc.off()
    spi.writebytes([cmd])

def data(data_bytes):
    dc.on()
    spi.writebytes(data_bytes)

# -----------------------------
# RESET DISPLAY
# -----------------------------
def reset():
    rst.on()
    time.sleep(0.1)
    rst.off()
    time.sleep(0.1)
    rst.on()
    time.sleep(0.1)

# -----------------------------
# INIT ILI9341
# -----------------------------
def init_display():
    reset()

    command(0x01)  # Software reset
    time.sleep(0.1)

    command(0x28)  # Display OFF

    command(0xCF)
    data([0x00, 0xC1, 0x30])

    command(0xED)
    data([0x64, 0x03, 0x12, 0x81])

    command(0xE8)
    data([0x85, 0x00, 0x78])

    command(0xCB)
    data([0x39, 0x2C, 0x00, 0x34, 0x02])

    command(0xF7)
    data([0x20])

    command(0xEA)
    data([0x00, 0x00])

    command(0xC0)
    data([0x23])

    command(0xC1)
    data([0x10])

    command(0xC5)
    data([0x3E, 0x28])

    command(0xC7)
    data([0x86])

    command(0x36)
    data([0x48])

    command(0x3A)
    data([0x55])

    command(0xB1)
    data([0x00, 0x18])

    command(0xB6)
    data([0x08, 0x82, 0x27])

    command(0xF2)
    data([0x00])

    command(0x26)
    data([0x01])

    command(0xE0)
    data([
        0x0F, 0x31, 0x2B, 0x0C,
        0x0E, 0x08, 0x4E, 0xF1,
        0x37, 0x07, 0x10, 0x03,
        0x0E, 0x09, 0x00
    ])

    command(0xE1)
    data([
        0x00, 0x0E, 0x14, 0x03,
        0x11, 0x07, 0x31, 0xC1,
        0x48, 0x08, 0x0F, 0x0C,
        0x31, 0x36, 0x0F
    ])

    command(0x11)  # Sleep OUT
    time.sleep(0.12)

    command(0x29)  # Display ON

# -----------------------------
# SET DRAW WINDOW
# -----------------------------
def set_window(x0, y0, x1, y1):
    command(0x2A)
    data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])

    command(0x2B)
    data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])

    command(0x2C)

# -----------------------------
# FILL SCREEN
# -----------------------------
def fill_screen(color):
    set_window(0, 0, WIDTH - 1, HEIGHT - 1)

    hi = color >> 8
    lo = color & 0xFF

    dc.on()

    chunk = [hi, lo] * 1024

    total_pixels = WIDTH * HEIGHT

    for _ in range(total_pixels // 1024):
        spi.writebytes(chunk)

# -----------------------------
# MAIN TEST
# -----------------------------
init_display()

while True:
    print("RED")
    fill_screen(0xF800)
    time.sleep(1)

    print("GREEN")
    fill_screen(0x07E0)
    time.sleep(1)

    print("BLUE")
    fill_screen(0x001F)
    time.sleep(1)

    print("WHITE")
    fill_screen(0xFFFF)
    time.sleep(1)
