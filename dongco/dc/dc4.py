import RPi.GPIO as GPIO
from time import sleep

# --- Cấu hình chân ---
ENA = 14   # Chân PWM điều khiển tốc độ
IN1 = 27   # Chân điều khiển chiều
IN2 = 22   # Chân điều khiển chiều

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# --- Tạo PWM trên ENA (tần số 1kHz) ---
pwm = GPIO.PWM(ENA, 1000)  # 1000Hz
pwm.start(0)  # bắt đầu với duty = 0 (motor dừng)

def forward(speed):
    """Quay thuận với tốc độ (0-100%)"""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def backward(speed):
    """Quay ngược với tốc độ (0-100%)"""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def stop():
    """Dừng motor"""
    pwm.ChangeDutyCycle(0)

try:
    while True:
        print("Quay thuận chậm (10%)")
        forward(10)
        sleep(2)
        stop()
        sleep(2)

        print("Tăng tốc (40%)")
        forward(40)
        sleep(1)

        print("Dừng 1s")
        stop()
        sleep(2)

        print("Quay ngược nhanh (80%)")
        backward(80)
        sleep(2)

        print("Quay ngược chậm (40%)")
        backward(40)
        sleep(2)

        print("Dừng 1s")
        stop()
        sleep(1)

except KeyboardInterrupt:
    print("Kết thúc bởi người dùng")
finally:
    pwm.stop()
    GPIO.cleanup()
