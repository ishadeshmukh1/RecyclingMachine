import time
from PIL import Image, ImageDraw, ImageFont
from python_ili9341 import Display, color565

# Update these if your wiring uses different GPIOs:
DC_PIN = 22   # GPIO22 (physical pin 15)
RST_PIN = 27  # GPIO27 (physical pin 13)
LED_PIN = None  # Leave None if LED is tied directly to 3.3V

# SPI0: SCLK on GPIO11 (pin 23), MOSI on GPIO10 (pin 19), CS on GPIO8 (pin 24)

def main():
    # Create display object
    display = Display(
        dc=DC_PIN,
        rst=RST_PIN,
        spi_port=0,
        spi_device=0,
        width=320,
        height=240,
        rotation=0
    )

    # Clear screen to black
    display.clear(color565(0, 0, 0))

    # Create an image to draw on
    image = Image.new("RGB", (320, 240), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw HELLO in the middle
    text = "HELLO"
    font = ImageFont.load_default()
    w, h = draw.textsize(text, font=font)
    x = (320 - w) // 2
    y = (240 - h) // 2

    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # Send image to display
    display.display(image)

    # Keep it on screen
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_ILI9341 as ILI9341

# UPDATE THESE TO MATCH YOUR GPIO NUMBERS
DC_PIN = 24   # GPIO24 if DC is on physical pin 18
RST_PIN = 25  # GPIO25 if RESET is on physical pin 22

# Raspberry Pi hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0

def main():
    # Create TFT LCD display object:
    disp = ILI9341.ILI9341(
        dc=DC_PIN,
        rst=RST_PIN,
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000)
    )

    # Initialize display
    disp.begin()

    # Clear to black
    disp.clear((0, 0, 0))

    # Create image buffer
    width, height = disp.width, disp.height
    image = Image.new("RGB", (width, height), (0, 0, 0))
import time
from PIL import Image, ImageDraw, ImageFont

import Adafruit_GPIO.SPI as SPI
import Adafruit_ILI9341 as ILI9341

# CHANGE these two to match your actual wiring:
DC_PIN = 24   # GPIO24 if DC/RS is on physical pin 18
RST_PIN = 25  # GPIO25 if RESET is on physical pin 22

SPI_PORT   = 0
SPI_DEVICE = 0

def main():
    disp = ILI9341.ILI9341(
        dc=DC_PIN,
        rst=RST_PIN,
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000)
    )

    disp.begin()
    disp.clear((0, 0, 0))

    width, height = disp.width, disp.height
    image = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    text = "HELLO"
    font = ImageFont.load_default()
    w, h = draw.textsize(text, font=font)
    x = (width - w) // 2
    y = (height - h) // 2
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    disp.display(image)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
