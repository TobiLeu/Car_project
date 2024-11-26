
import machine
import time
import network
import espnow
from machine import ADC
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
### Code Sender

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      

e = espnow.ESPNow()
e.active(True)
peer = b'\x88\x13\xbf\x6f\xb9\xbc'   # MAC address of receiver  88:13:bf:6f:b9:bc
e.add_peer(peer)      # Must add_peer() before send()

adc1 = ADC(36)
adc1.atten(ADC.ATTN_11DB) #Messbereich auf 
adc2 = ADC(39)
adc2.atten(ADC.ATTN_11DB)


# ESP am Auto rebooten: 5 Sekunden warten auf Reboot
msg= b'0,0,1'
e.send(peer, msg, True)
print(msg)
time.sleep(5)


while True:
    val1 = adc1.read_u16()
    val2 = adc2.read_u16()
    msg = ",".join([str(val1),str(val2),"0"])
    
    print(msg)

    e.send(peer, msg , True)
    time.sleep_ms(50)

