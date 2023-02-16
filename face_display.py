from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# OLED width 16 characters
# OLED height 8 characters

happy = [
        "                ",
        "                ",
        "    ^       ^   ",
        "    0       0   ",
        "        v       ",
        "                ",
        "                ",
        "                ",
]

sad = [
        "                ",
        "                ",
        "    ^       ^   ",
        "    0       0   ",
        "        ^       ",
        "                ",
        "                ",
        "                ",
]

left = [
        "                ",
        "                ",
        "   ^       ^    ",
        "   0       0    ",
        "         v      ",
        "                ",
        "                ",
        "                ",
]

right = [
        "                ",
        "                ",
        "     ^       ^  ",
        "     0       0  ",
        "       v        ",
        "                ",
        "                ",
        "                ",
]


off = [
        "                ",
        "                ",
        "                ",
        "   _        _   ",
        "                ",
        "       __       ",
        "                ",
        "                ",
]

idle = [
        "                ",
        "                ",
        "    ^       ^   ",
        "    0       0   ",
        "        _       ",
        "                ",
        "                ",
        "                ",
]


modes = {
    "happy" : happy,
    "sad" : sad,
    "left" : left,
    "right" : right,
    "idle" : idle,
}

def set_face(mode):
    face = modes.get(mode)
    oled.fill(0)
    
    for j in range(len(face)):
        oled.text(face[j],0,j*8)
        
    oled.show()

def off_face():
    oled.fill(0)
    
    for j in range(len(off)):
        oled.text(off[j],0,j*8)
        
    oled.show()
