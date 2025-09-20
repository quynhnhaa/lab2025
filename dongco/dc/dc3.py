import RPi.GPIO as GPIO
from time import sleep

ENA, IN1, IN2 = 17, 27, 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# PWM để điều khiển tốc độ (1kHz)
pwm = GPIO.PWM(ENA, 1000)
pwm.start(100)  # 100% duty = full speed

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

try:
    while True:
        forward()
        sleep(1)
        backward()
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
