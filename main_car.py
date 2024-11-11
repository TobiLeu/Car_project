from machine import Pin, ADC, PWM
import time

motor_1_IN1 = Pin(22, Pin.OUT)
motor_1_IN2 = Pin(23, Pin.OUT)
motor_1_pwm = PWM(Pin(32), freq=250, duty=0)
motor_2_IN3 = Pin(27, Pin.OUT)
motor_2_IN4 = Pin(14, Pin.OUT)
motor_2_pwm = PWM(Pin(12), freq=250, duty = 0)
adc1 = ADC(36)
adc1.atten(ADC.ATTN_11DB) #Messbereich auf 
adc2 = ADC(39)
adc2.atten(ADC.ATTN_11DB)

def convert_16bit_to_10bit(value_16bit):
    
    if not (0 <= value_16bit <= 65535):
        raise ValueError("Die Eingabewert muss zwischen 0 und 65535 liegen.")
    
    # Skalieren des 16-Bit-Wertes in den Bereich einer 10-Bit-Zahl
    value_10bit = int((value_16bit / 65535) * 1023)
    
    return value_10bit

def calc_dutycycle_forward(analog):
    dutycycle = 256 +(analog-530)*(1023-256)/(1023-530) #lineare Transfortmation für PWM
    return int(dutycycle)

def calc_dutycycle_reverse(analog):
    dutycycle = 1023 +(analog-0)*(256-1023)/(494-0) #lineare Transfortmation für PWM
    return int(dutycycle)


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
    
while True:
    val1 = adc1.read_u16()
    val2 = adc2.read_u16()
    joystick1 = convert_16bit_to_10bit(val1)
    joystick2 = convert_16bit_to_10bit(val2)
    left_track(joystick1)
    right_track(joystick2)