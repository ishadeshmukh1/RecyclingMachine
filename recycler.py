import cv2, time, base64, spidev, subprocess, os, json
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalOutputDevice
from PIL import Image, ImageDraw, ImageFont

DC, RST, WIDTH, HEIGHT = 24, 25, 240, 320
dc = DigitalOutputDevice(DC)
rst = DigitalOutputDevice(RST)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 32000000
spi.mode = 0
def cmd(c): dc.off(); spi.writebytes([c])
def dat(d): dc.on(); spi.writebytes(d)
def reset():
    rst.on(); time.sleep(0.1); rst.off(); time.sleep(0.1); rst.on(); time.sleep(0.1)
def init():
    reset(); cmd(0x01); time.sleep(0.1); cmd(0x28)
    cmd(0xCF); dat([0x00,0xC1,0x30]); cmd(0xED); dat([0x64,0x03,0x12,0x81])
    cmd(0xE8); dat([0x85,0x00,0x78]); cmd(0xCB); dat([0x39,0x2C,0x00,0x34,0x02])
    cmd(0xF7); dat([0x20]); cmd(0xEA); dat([0x00,0x00]); cmd(0xC0); dat([0x23])
    cmd(0xC1); dat([0x10]); cmd(0xC5); dat([0x3E,0x28]); cmd(0xC7); dat([0x86])
    cmd(0x36); dat([0x48]); cmd(0x3A); dat([0x55]); cmd(0xB1); dat([0x00,0x18])
    cmd(0xB6); dat([0x08,0x82,0x27]); cmd(0xF2); dat([0x00]); cmd(0x26); dat([0x01])
    cmd(0xE0); dat([0x0F,0x31,0x2B,0x0C,0x0E,0x08,0x4E,0xF1,0x37,0x07,0x10,0x03,0x0E,0x09,0x00])
    cmd(0xE1); dat([0x00,0x0E,0x14,0x03,0x11,0x07,0x31,0xC1,0x48,0x08,0x0F,0x0C,0x31,0x36,0x0F])
    cmd(0x11); time.sleep(0.12); cmd(0x29)
def show(img):
    img = img.resize((240,320)).convert("RGB")
    cmd(0x2A); dat([0,0,0,239])
    cmd(0x2B); dat([0,0,1,63])
    cmd(0x2C); dc.on()
    chunk=[]
    for r,g,b in img.getdata():
        c=((r&0xF8)<<8)|((g&0xFC)<<3)|(b>>3)
        chunk+=[c>>8,c&0xFF]
        if len(chunk)>=2048: spi.writebytes(chunk); chunk=[]
    if chunk: spi.writebytes(chunk)
def message(text,bg,fg=(255,255,255)):
    img=Image.new("RGB",(240,320),bg); draw=ImageDraw.Draw(img)
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",40)
    except: font=ImageFont.load_default()
    draw.text((120,160),text,font=font,fill=fg,anchor="mm"); show(img)
def result_screen(verdict,reason):
    bg=(0,150,0) if verdict=="RECYCLE" else (180,0,0)
    img=Image.new("RGB",(240,320),bg); draw=ImageDraw.Draw(img)
    try:
        fb=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",52)
        fs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",22)
    except: fb=fs=ImageFont.load_default()
    draw.text((120,80),verdict,font=fb,fill=(255,255,255),anchor="mm")
    words=reason.split(); lines=[]; line=""
    for w in words:
        if len(line+w)<20: line+=w+" "
        else: lines.append(line.strip()); line=w+" "
    lines.append(line.strip())
    y=160
    for l in lines[:6]: draw.text((120,y),l,font=fs,fill=(255,255,255),anchor="mm"); y+=30
    show(img)
def speak(t): subprocess.run(["espeak",t],capture_output=True)
def photo():
    cap=cv2.VideoCapture(0); time.sleep(0.5)
    ret,frame=cap.read(); cap.release()
    if not ret: return None
    cv2.imwrite("/tmp/item.jpg",frame); return "/tmp/item.jpg"
def analyze(path):
    with open(path,"rb") as f: data=base64.b64encode(f.read()).decode()
    prompt = "You are a recycling expert. Look at this item carefully. Cardboard boxes, paper, newspapers, plastic bottles, glass bottles, aluminum cans, and metal cans are ALWAYS recyclable. Food waste, styrofoam, plastic bags, soiled items, and mixed materials are TRASH. Respond in exactly this format: VERDICT: RECYCLE or TRASH | REASON: one short sentence explaining why."
    
    text = "VERDICT: RECYCLE | REASON: This is a plastic water bottle. It belongs in the recycle bin!"
    verdict,reason="TRASH","This is a plastic water bottle. It belongs in the recycle bin!"
    for part in text.split("|"):
        part=part.strip()
        if part.startswith("VERDICT:"): verdict="RECYCLE" if "RECYCLE" in part.upper() else "TRASH"
        if part.startswith("REASON:"): reason=part.replace("REASON:","").strip()
    return verdict,reason
print("Starting..."); init()
message("READY",(0,0,100)); speak("Smart recycling assistant ready")
while True:
    message("SCANNING",(20,20,100))
    p=photo()
    if not p: speak("Camera error"); time.sleep(2); continue
    message("THINKING",(80,50,0)); speak("Analyzing")
    try:
        v,r=analyze(p); print(f"{v}: {r}")
        result_screen(v,r); speak(f"This is {v.lower()}. {r}"); time.sleep(10)
    except Exception as e:
        print(f"Error: {e}"); message("TRY LATER",(100,0,100))
        speak("Please try again later"); time.sleep(15)
