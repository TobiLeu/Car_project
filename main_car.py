from machine import Pin, ADC, PWM
import machine
import time
import network 
import espnow


# MAC-Adresse des ESP32: 88:13:bf:6f:b9:bc

#Setup PINS

motor_1_IN1 = Pin(22, Pin.OUT)
motor_1_IN2 = Pin(23, Pin.OUT)
motor_1_pwm = PWM(Pin(32), freq=250, duty=0)
motor_2_IN3 = Pin(27, Pin.OUT)
motor_2_IN4 = Pin(14, Pin.OUT)
motor_2_pwm = PWM(Pin(12), freq=250, duty = 0)

#Setup WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()   # Because ESP8266 auto-connects to last Access Point

#ESP Now Setup
e = espnow.ESPNow()
e.active(True)

#ADC 
death_zone_upper_limit = 530
death_zone_lower_limt = 400
pwm_start = 256
pwm_end = 1023




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
        motor_1_IN1.on()
        motor_1_IN2.off()
        motor_1_pwm.duty(map_range_forward(analog_In_l, death_zone_upper_limit, 1023, pwm_start, pwm_end))
    
    elif analog_In_l < death_zone_lower_limt :
        motor_1_IN1.off()  
        motor_1_IN2.on()
        motor_1_pwm.duty(map_range_backward(analog_In_l,death_zone_lower_limt, 0, pwm_start, pwm_end))
    
    else:
        motor_1_IN1.off()
        motor_1_IN2.off()
        motor_1_pwm.duty(0)

# Steuerung rechte Kette

def right_track(analog_In_r):
    if analog_In_r > death_zone_upper_limit:
        motor_2_IN3.on()
        motor_2_IN4.off()
        motor_2_pwm.duty(map_range_forward(analog_In_r, death_zone_upper_limit, 1023, pwm_start, pwm_end))

    elif analog_In_r < death_zone_lower_limt :
        motor_2_IN3.off()  
        motor_2_IN4.on()
        motor_2_pwm.duty(map_range_backward(analog_In_r, death_zone_lower_limt, 0, pwm_start, pwm_end))
    
    else:
        motor_2_IN3.off()
        motor_2_IN4.off()
        motor_2_pwm.duty(0)

# Hauptschleife  
while True:
    #host, msg = e.recv()
    if msg = e.recv():  #msg == None if timeout in recv()
        print(msg)
        msg =str(msg)
        msg = msg.lstrip("b'")
        msg = msg.rstrip("'")
        values = msg.split(",")
        value1 = int(values[0])
        value2 = int(values[1])
        value3 = int(values[2])
        value1 = convert_16bit_to_10bit(value1)
        value2 = convert_16bit_to_10bit(value2)

        if value3 == 3:
            print("rebooting")
            machine.reset()

        left_track(value1)
        right_track(value2)
        time.sleep(0.001)