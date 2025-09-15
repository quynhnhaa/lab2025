# /Users/quynhnhaa/Documents/Ahn/Study/Year4.1/IoT/lab2025/dongco/test_dc_basic.py
import RPi.GPIO as GPIO
import time

ENA = 21
IN1 = 20
IN2 = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm = GPIO.PWM(ENA, 100)
pwm.start(100)  # 100% duty để loại trừ vấn đề PWM

try:
    print("Forward 3s")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(3)

    print("Stop 1s")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(1)

    print("Backward 3s")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(3)

    print("Stop")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
finally:
    pwm.stop()
    GPIO.cleanup()
