
import machine
import time
import network
import espnow
from machine import ADC,Pin
from lcd1602 import LCD1602
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
### Datenübertragung initialisieren

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      

e = espnow.ESPNow()
e.active(True)
peer = b'\x88\x13\xbf\x6f\xb9\xbc'   # MAC address of receiver  88:13:bf:6f:b9:bc
e.add_peer(peer)      # Must add_peer() before send()


# Pins definieren

adc2 = ADC(36)
adc2.atten(ADC.ATTN_11DB) #Messbereich auf 
adc1 = ADC(39)
adc1.atten(ADC.ATTN_11DB)

button = Pin(25, Pin.IN, Pin.PULL_UP)
light = 0


########################################################################################## 
    #LCD Display
 
#ADC 
death_zone_upper_limit = 530
death_zone_lower_limt = 400
pwm_start = 256
pwm_end = 1023

### Berechnungsfunktionen für die Displayanzeige

# 16bit Eingang zu 10 bit konvertieren
def convert_16bit_to_10bit(value_16bit):
    
    if not (0 <= value_16bit <= 65535):
        raise ValueError("Die Eingabewert muss zwischen 0 und 65535 liegen.")
    
    # Skalieren des 16-Bit-Wertes in den Bereich einer 10-Bit-Zahl
    value_10bit = int((value_16bit / 65535) * 1023)
    
    return value_10bit

# PWM signal for forward drive
def map_range_forward(value, in_min, in_max, out_min, out_max):
    """
    Rechnet einen Wert aus einem Bereich in einen anderen Bereich um.

    :param value: Der Eingabewert, der umgerechnet werden soll.
    :param in_min: Untere Grenze des Eingabebereichs.
    :param in_max: Obere Grenze des Eingabebereichs.
    :param out_min: Untere Grenze des Zielbereichs.
    :param out_max: Obere Grenze des Zielbereichs.
    :return: Der umgerechnete Wert im Zielbereich.
    """
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min



def map_range_backward(value, in_min, in_max, out_min, out_max):
    """
    Rechnet einen Wert aus einem Bereich in einen anderen Bereich um.
    :param value: Der Eingabewert, der umgerechnet werden soll.
    :param in_min: Untere Grenze des Eingabebereichs.
    :param in_max: Obere Grenze des Eingabebereichs.
    :param out_min: Untere Grenze des Zielbereichs.
    :param out_max: Obere Grenze des Zielbereichs.
    :return: Der umgerechnete Wert im Zielbereich.
    """
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def left_track (analog_In_l):
    if analog_In_l > death_zone_upper_limit :
        
        return map_range_forward(analog_In_l, death_zone_upper_limit, 1023, pwm_start, pwm_end)
    
    elif analog_In_l < death_zone_lower_limt :
        
        return map_range_backward(analog_In_l,death_zone_lower_limt, 0, pwm_start, pwm_end)
    
    else:    
        return 0

def map_to_percentage(value, start=pwm_start, end=pwm_end):
    """
    Wandelt einen Wert aus dem Bereich [256, 1023] in einen Prozentsatz [1, 100] um.
    Wenn der Wert 0 ist, wird 0% zurückgegeben.
    
    :param value: Der Eingabewert, der in Prozent umgerechnet werden soll.
    :param start: Der Anfangswert des Bereichs (256 entspricht 1%).
    :param end: Der Endwert des Bereichs (1023 entspricht 100%).
    :return: Der Wert als Prozentsatz (zwischen 0 und 100).
    """
    if value == 0:
        return 0  # 0 ergibt 0%
    

    # Prozentwert berechnen
    percentage = (value - start) * (100 - 1) / (end - start) + 1
    return round(percentage)
   

# LCD initialisieren 
lcd = LCD1602(rs=4, e=5, d4=16, d5=17, d6=18, d7=19) # Nummern in der Funktion entsprechen den verwendeten Pins

######################################################################################################


# ESP am Auto rebooten: 5 Sekunden warten auf Reboot
msg= b'30000,30000,1,0'
e.send(peer, msg, True)
print(msg)
time.sleep(5)

######################################################################################################

#Programmschleife

while True:
    val1 = adc1.read_u16()
    val2 = adc2.read_u16()

    #Umrechnen der Eingangswerte für das Display
    value_left_joystick = convert_16bit_to_10bit(val1)
    value_left_display = left_track(value_left_joystick) 
    
    value_right_joystick = convert_16bit_to_10bit(val2)
    value_right_display = left_track(value_right_joystick) 

    Displaywert_Kette_links = map_to_percentage(value_left_display)
    Diplaywert_Kette_rechts = map_to_percentage(value_right_display)

    # Anzeige Display
    lcd.clear()
    lcd.write(0, 0, f"Links     Rechts")
    lcd.write(1, 0, f"{Displaywert_Kette_links}%        {Diplaywert_Kette_rechts}%")
    

    # Taster prüfen (LOW = gedrückt)
    if button.value() == 0:
        while button.value() == 0:
            pass  
        
        # LED-Zustand umschalten
        light = 1 - light
   
    #Erstellen und Senden der Nachricht an den ESP Auto
    msg = ",".join([str(val1),str(val2),"0",str(light)])
    e.send(peer, msg , True)

    time.sleep_ms(50)