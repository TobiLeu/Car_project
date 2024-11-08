from machine import Pin, PWM
import time

motor_1_IN1 = Pin(34, Pin.OUT)
motor_1_IN2 = Pin(35, Pin.OUT)
motor_1_pwm = PWM(Pin(32), freq=250, duty=0)
motor_2_IN3 = Pin(27, Pin.OUT)
motor_2_IN4 = Pin(14, Pin.OUT)
motor_2_pwm = PWM(Pin(12), freq=250, duty = 0)


def move_forward(dutycycle):
    motor_1_IN1.off()
    motor_1_IN2.on()
    motor_1_pwm.duty(dutycycle)
    motor_2_IN3.on()
    motor_2_IN4.off()
    motor_2_pwm(dutycycle)


    
while True:
    move_forward(512)
