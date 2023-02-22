import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket

from dd_motor import move_bot, ENA, ENB
from face_display import oled

rl = machine.Pin(3,machine.Pin.OUT)
yl = machine.Pin(4,machine.Pin.OUT)
gl = machine.Pin(5,machine.Pin.OUT)


# Set country to avoid possible errors
rp2.country('PL')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    if num_blinks < 0:
        for i in range(5):
            rl.value(1)
            time.sleep(.2)
            rl.value(0)
            time.sleep(.2)
    elif num_blinks < 3:
        for i in range(5):
            yl.value(1)
            time.sleep(.2)
            yl.value(0)
            time.sleep(.2)
    else:
        for i in range(5):
            gl.value(1)
            time.sleep(.2)
            gl.value(0)
            time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)

# Listen for connections
def server_handle():
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        
        forw = True
        moves = []
        
        dd_go = r.find('?dd=go')
        dd_left = r.find('?dd=left')
        dd_right = r.find('?dd=right')
        
        dd_bgo = r.find('?dd=bgo')
        dd_bleft = r.find('?dd=bleft')
        dd_bright = r.find('?dd=bright')
        
        dd_stop = r.find('?dd=stop')
        turn_off = r.find('?dd=off')
        
        if turn_off == 10:
            raise KeyboardInterrupt
        
        if dd_bgo == 10 or dd_bleft == 10 or dd_bright == 10:
            forw = False
            moves = [dd_bgo, dd_stop, dd_bleft, dd_bright]
        else:
            moves = [dd_go, dd_stop, dd_left, dd_right]

        for i in range(len(moves)):
            if moves[i] < 0:
                moves[i] = False
            else:
                moves[i] = True
                 
        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
        move_bot(moves[0], moves[1], moves[2], moves[3], forw)
        return True
        
    except OSError as e:
        print(e)
        cl.close()
        print('Connection closed')
        rl.value(1)
        time.sleep(2)
        rl.value(0)
        ENA.low()
        ENB.low()
        return False
    
    except KeyboardInterrupt:
        yl.value(1)
        time.sleep(2)
        yl.value(0)
        ENA.low()
        ENB.low()
        return False
    
    except Exception as e:
        rl.value(1)
        time.sleep(2)
        rl.value(0)
        oled.text(e,0,0)
        oled.show()
        ENA.low()
        ENB.low()
        return False

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()
