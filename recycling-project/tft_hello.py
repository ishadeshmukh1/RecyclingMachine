import time
from PIL import Image, ImageDraw, ImageFont

import Adafruit_ILI9341 as ILI9341
import Adafruit_GPIO.SPI as SPI

# Raspberry Pi hardware SPI config:
SPI_PORT = 0        # SPI0
SPI_DEVICE = 0      # CE0 (pin 24)
DC = 22             # GPIO22, pin 15
RST = 27            # GPIO27, pin 13

# Create TFT LCD display object.
disp = ILI9341.ILI9341(dc=DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
disp.begin()

# Get display size.
width = disp.width
height = disp.height

# Create a new image with RGB mode and a black background.
image = Image.new('RGB', (width, height), (0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw "HELLO" in the middle of the screen.
text = "HELLO"
# Simple default font.
font = ImageFont.load_default()

# Measure text size.
text_width, text_height = draw.textsize(text, font=font)
x = (width - text_width) // 2
y = (height - text_height) // 2

# Draw text in white.
draw.text((x, y), text, font=font, fill=(255, 255, 255))

# Display image.
disp.display(image)

# Keep it on screen.
while True:
    time.sleep(1)
