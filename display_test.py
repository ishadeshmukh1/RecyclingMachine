import board, busio, digitalio
from adafruit_rgb_display import ili9341
from PIL import Image, ImageDraw

cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D24)
rst = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
display = ili9341.ILI9341(spi, cs=cs, dc=dc, rst=rst, width=320, height=240)
image = Image.new('RGB', (320, 240), color=(0, 180, 0))
draw = ImageDraw.Draw(image)
draw.text((60, 100), 'DISPLAY WORKS!', fill=(255, 255, 255))
display.image(image)
print('Display test done!')
