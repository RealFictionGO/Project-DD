from machine import Pin
from face_display import set_face

ldc = Pin(14,Pin.OUT)
rdc = Pin(17,Pin.OUT)

def move_bot(go, stop, left, right):
    if stop == True:
        ldc.value(0)
        rdc.value(0)
        set_face("idle")
    elif go == True:
        ldc.value(1)
        rdc.value(1)
        set_face("happy")
    elif left == True:
        ldc.value(1)
        rdc.value(0)
        set_face("left")
    elif right == True:
        ldc.value(0)
        rdc.value(1)
        set_face("right")
