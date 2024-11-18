
import machine
import time
import network
import espnow
'''
# WLAN-Station (Client) Schnittstelle initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# MAC-Adresse abrufen
mac_address = wlan.config('mac')
mac_address_str = ':'.join(['{:02x}'.format(b) for b in mac_address])

# MAC-Adresse ausgeben
print("MAC-Adresse des ESP32:", mac_address_str)
'''

'''
### Code Sender

import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xac\x15\x18\xe9\x8c\x7c'   # MAC address of peer's wifi interface  ac:15:18:e9:8c:7c
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")
for i in range(100):
    e.send(peer, str(i)*20, True)
e.send(peer, b'end')

'''
### Code Empfänger

import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'end':
            break