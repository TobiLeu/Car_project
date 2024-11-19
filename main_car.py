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
########################
# Dutycile für PWM berechnen 
def calc_dutycycle_forward(analog):
    dutycycle = 256 + (analog-530)*(1023-256)/(65535-530) #lineare Transfortmation für PWM
    print(f"d1:{dutycycle}")
    return int(dutycycle)

def calc_dutycycle_reverse(analog):
    dutycycle = 256 + (analog-0)*(256-65535)/(494-0) #lineare Transfortmation für PWM
    print(f"d2:{dutycycle}")
    return int(dutycycle)
 ############################


def calc_dutycycle_with_deadzone_16to10bit(analog):
    """
    Berechnet den PWM-Duty-Cycle (10-Bit) aus einem 16-Bit-Eingangswert mit einem Totraum von ±10%.
    
    Parameters:
        analog (int): Eingabewert, erwartet im Bereich [0, 65535].
    
    Returns:
        int: PWM-Duty-Cycle, im Bereich [0, 1023].
    """
    # 16-Bit-Mittelwert und Totraumgrenzen berechnen
    pwm_middle = 32768
    deadzone_offset = int(pwm_middle * 0.1)  # 10% von 32768 = 3276.8
    lower_deadzone = pwm_middle - deadzone_offset  # 26215
    upper_deadzone = pwm_middle + deadzone_offset  # 39321
    
    # Bereichsprüfung
    if analog < 0 or analog > 65535:
        raise ValueError("Der Eingabewert 'analog' muss im Bereich [0, 65535] liegen.")
    
    if analog < lower_deadzone:
        # Unterhalb des Totraums: Linear auf [0, lower_deadzone] → [0, 511]
        return int((analog / lower_deadzone) * 511)
    elif analog > upper_deadzone:
        # Oberhalb des Totraums: Linear auf [upper_deadzone, 65535] → [512, 1023]
        return int(512 + ((analog - upper_deadzone) / (65535 - upper_deadzone)) * 511)
    else:
        # Innerhalb des Totraums
        if analog < pwm_middle:
            return 0  # Unterhalb des Mittelwerts
        else:
            return 1023  # Oberhalb des Mittelwerts

# Steuerung linke Kette

def left_track (analog_In):
    if analog_In > 35000:
        motor_1_IN1.on()
        motor_1_IN2.off()
        x1 = calc_dutycycle_with_deadzone_16to10bit(analog_In)
        print(f"{x1}")
        motor_1_pwm.duty(x1)
    elif analog_In < 29000 :
        motor_1_IN1.off()  
        motor_1_IN2.on()
        x2 = calc_dutycycle_with_deadzone_16to10bit(analog_In)
        print(f"{x2}")
        motor_1_pwm.duty(x2)
    else:
        motor_1_IN1.on()
        motor_1_IN2.on()
        motor_1_pwm.duty(0)

# Steuerung rechte Kette

def right_track(analog_In):
    if analog_In > 32000:
        motor_2_IN3.on()
        motor_2_IN4.off()
        motor_2_pwm.duty(calc_dutycycle_with_deadzone_16to10bit(analog_In))
    elif analog_In < 29000 :
        motor_2_IN3.off()  
        motor_2_IN4.on()
        motor_2_pwm.duty(calc_dutycycle_with_deadzone_16to10bit(analog_In))
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
        msg = msg.lstrip("b'")
        msg = msg.rstrip("'")
        values = msg.split(",")
        value1 = int(values[0])
        value2 = int(values[1])
        print(values)
        print(value1)   
        print(value2)
    left_track(value1)
    right_track(value2)