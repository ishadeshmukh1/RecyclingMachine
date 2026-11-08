import board
import busio
import digitalio
from adafruit_rgb_display import ili9341
from PIL import Image, ImageDraw, ImageFont

# Display setup
cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D24)
rst = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI, MISO=board.MISO)

display = ili9341.ILI9341(spi, cs=cs, dc=dc, rst=rst, width=320, height=240)

# Draw a green screen to test
image = Image.new("RGB", (320, 240), color=(0, 200, 0))
draw = ImageDraw.Draw(image)
draw.text((80, 100), "DISPLAY WORKS!", fill=(255, 255, 255))
display.image(image)
