import board
import busio
from digitalio import DigitalInOut, Direction
from adafruit_ili9341 import ILI9341
from PIL import Image, ImageDraw, ImageFont

# SPI setup
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Control pins
cs_pin = DigitalInOut(board.CE0)    # GPIO8
dc_pin = DigitalInOut(board.D25)    # GPIO25
reset_pin = DigitalInOut(board.D23) # GPIO23

display = ILI9341(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, width=320, height=240)

# Create a blank image to draw on
image = Image.new("RGB", (320, 240), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw simple text
draw.text((40, 100), "HELLO", fill=(255, 255, 255))

# Show on display
display.image(image)
