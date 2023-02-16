from machine import Pin

import server
import face_display
from dd_motor import move_bot

while True:
    wserver = server.server_handle()
    
    if wserver == False:
        print("*** Connection Ended ***")
        break
    
face_display.off_face()