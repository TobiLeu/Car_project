from machine import Pin, ADC, PWM
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
#ADC Pins Joystick
adc1 = ADC(36)
adc1.atten(ADC.ATTN_11DB) #Messbereich auf 3.3V
adc2 = ADC(39)
adc2.atten(ADC.ATTN_11DB)

#Setup WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()   # Because ESP8266 auto-connects to last Access Point

#ESP Now Setup
e = espnow.ESPNow()
e.active(True)

#########################Nicht mehr notewendig
# 16bit Eingang zu 10 bit konvertieren
def convert_16bit_to_10bit(value_16bit):
    
    if not (0 <= value_16bit <= 65535):
        raise ValueError("Die Eingabewert muss zwischen 0 und 65535 liegen.")
    
    # Skalieren des 16-Bit-Wertes in den Bereich einer 10-Bit-Zahl
    value_10bit = int((value_16bit / 65535) * 1023)
    
    return value_10bit
####################

# Dutycile für PWM berechnen 
def calc_dutycycle_forward(analog):
    dutycycle = 256 + (analog-530)*(1023-256)/(65535-530) #lineare Transfortmation für PWM
    return int(dutycycle)

def calc_dutycycle_reverse(analog):
    dutycycle = 1023 + (analog-0)*(256-65535)/(494-0) #lineare Transfortmation für PWM
    return int(dutycycle)

# Steuerung linke Kette

def left_track (analog_In):
    if analog_In > 530:
        motor_1_IN1.on()
        motor_1_IN2.off()
        motor_1_pwm.duty(calc_dutycycle_forward(analog_In))
    elif analog_In < 494 :
        motor_1_IN1.off()  
        motor_1_IN2.on()
        motor_1_pwm.duty(calc_dutycycle_reverse(analog_In))
    else:
        motor_1_IN1.on()
        motor_1_IN2.on()
        motor_1_pwm.duty(0)

# Steuerung rechte Kette

def right_track(analog_In):
    if analog_In > 530:
        motor_2_IN3.on()
        motor_2_IN4.off()
        motor_2_pwm.duty(calc_dutycycle_forward(analog_In))
    elif analog_In < 494 :
        motor_2_IN3.off()  
        motor_2_IN4.on()
        motor_2_pwm.duty(calc_dutycycle_reverse(analog_In))
    else:
        motor_2_IN3.on()
        motor_2_IN4.on()
        motor_2_pwm.duty(0)

# Hauptschleife  
while True:
    host, msg = e.recv()
    if msg:  #msg == None if timeout in recv()
        print(msg)
        msg =str(msg)
        values = msg.split(",")
        value1 = values[0]
        value2 = values[1]
        print(values)
        print(value1)   
        print(value2)
    left_track(0)