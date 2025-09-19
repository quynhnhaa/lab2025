# # /Users/quynhnhaa/Documents/Ahn/Study/Year4.1/IoT/lab2025/dongco/test_dc_basic.py
# import RPi.GPIO as GPIO
# import time

# ENA = 21
# IN1 = 20
# IN2 = 16

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(ENA, GPIO.OUT)
# GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)

# pwm = GPIO.PWM(ENA, 100)
# pwm.start(100)  # 100% duty để loại trừ vấn đề PWM

# try:
#     print("Forward 3s")
#     GPIO.output(IN1, GPIO.HIGH)
#     GPIO.output(IN2, GPIO.LOW)
#     time.sleep(3)

#     print("Stop 1s")
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.LOW)
#     time.sleep(1)

#     print("Backward 3s")
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.HIGH)
#     time.sleep(3)

#     print("Stop")
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.LOW)
# finally:
#     pwm.stop()
#     GPIO.cleanup()

import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Khai báo chân
IN1 = 17
IN2 = 27
ENA = 22

# Thiết lập chân là output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Tạo PWM trên chân ENA với tần số 1000Hz
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)  # Bắt đầu với duty cycle = 0

def forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

try:
    print("Forward 50%")
    forward(50)
    time.sleep(5)

    print("Stop")
    stop()
    time.sleep(2)

    print("Backward 100%")
    backward(100)
    time.sleep(5)

    print("Stop")
    stop()

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    pwm.stop()
    GPIO.cleanup()
