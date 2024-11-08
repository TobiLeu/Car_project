import machine
import time
import network 

# WLAN-Station (Client) Schnittstelle initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# MAC-Adresse abrufen
mac_address = wlan.config('mac')
mac_address_str = ':'.join(['{:02x}'.format(b) for b in mac_address])

# MAC-Adresse ausgeben
print("MAC-Adresse des ESP32:", mac_address_str)


# Programm ESP32 Test
'''
    Für den Aufbau eine rote LED verwenden; 1,8V Druchlassspannung; Strom durch Diode 20mA; ESP Strom Output max 12mA
    ESP hat 3,3V Output. Vorwiderstand R= 3,3V/12mA = 275 Ohm -> 300 Ohm
'''

### Controller 1:
signal = False

led_red = machine.Pin(18, machine.Pin.OUT)

# Funktion zum Ein-/Ausschalten der LED
def receiver_led():   
    if signal:
        led_red.on()
    else:
        led_red.off()


### Controller 2: Button mit GND auf den Pin 2 legen

btn = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
signal = 0

# Funktion für Tasterabfrage:
def sender_button():
    
    if btn.value() == 0 and signal == 0:
        signal = 1
        time.delay(5)
    
    if btn.value() == 0 and signal == 1:
        signal = 0
        time.delay(5)
    



