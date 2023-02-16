import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket

from dd_motor import move_bot
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
        dd_go = r.find('?dd=go')
        dd_stop = r.find('?dd=stop')
        dd_left = r.find('?dd=left')
        dd_right = r.find('?dd=right')
        
        print(dd_go)
        print(dd_stop)
        print(dd_left)
        print(dd_right)
        
        if dd_go == 10:
            dd_go = True
            
        elif dd_left == 10:
            dd_left = True
            
        elif dd_right == 10:
            dd_right = True
            
        elif dd_stop == 10:
            dd_stop = True

        move_bot(dd_go, dd_stop, dd_left, dd_right)
            
        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        return True
        
    except OSError as e:
        print(e)
        cl.close()
        print('Connection closed')
        rl.value(1)
        time.sleep(2)
        rl.value(0)
        return False
    
    except KeyboardInterrupt:
        yl.value(1)
        time.sleep(2)
        yl.value(0)
        return False
    
    except Exception as e:
        rl.value(1)
        time.sleep(2)
        rl.value(0)
        oled.text(e)
        oled.show()
        return False

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()
