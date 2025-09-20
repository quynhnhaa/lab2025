import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Khai báo chân
ENA = 13
IN1 = 19
IN2 = 26


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
    print("Forward 30%")
    forward(30)
    time.sleep(5)

    print("Stop")
    stop()
    time.sleep(2)

    print("Backward 30%")
    backward(30)
    time.sleep(5)

    print("Stop")
    stop()

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    pwm.stop()
    GPIO.cleanup()
