from machine import Pin
from face_display import set_face

ldc = Pin(14,Pin.OUT)
ldc2 = Pin(15,Pin.OUT)

rdc = Pin(17,Pin.OUT)
rdc2 = Pin(16,Pin.OUT)

ENA = Pin(13,Pin.OUT)
ENB = Pin(18,Pin.OUT)

def move_bot(go, stop, left, right, forw):
    if stop == True:
        ldc.value(0)
        ldc2.value(0)
        rdc.value(0)
        rdc2.value(0)
        ENA.low()
        ENB.low()
        set_face("idle")
    
    elif forw == True:
        
        if go == True:
            ldc.value(0)
            ldc2.value(1)
            rdc.value(0)
            rdc2.value(1)
            ENA.high()
            ENB.high()
            set_face("happy")
        elif left == True:
            ldc.value(0)
            ldc2.value(0)
            rdc.value(0)
            rdc2.value(1)
            ENA.low()
            ENB.high()
            set_face("left")
        elif right == True:
            ldc.value(0)
            ldc2.value(1)
            rdc.value(0)
            rdc2.value(0)
            ENA.high()
            ENB.low()
            set_face("right")
            
            
    elif forw == False:
        
        if go == True:
            ldc.value(1)
            ldc2.value(0)
            rdc.value(1)
            rdc2.value(0)
            ENA.high()
            ENB.high()
            set_face("happy")
        elif left == True:
            ldc.value(0)
            ldc2.value(0)
            rdc.value(1)
            rdc2.value(0)
            ENA.low()
            ENB.high()
            set_face("left")
        elif right == True:
            ldc.value(1)
            ldc2.value(0)
            rdc.value(0)
            rdc2.value(0)
            ENA.high()
            ENB.low()
            set_face("right")