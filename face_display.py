from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def set_face():
    pass

def off_face():
    pass