import RPi.GPIO as GPIO
import time

# Gán chân GPIO (theo BCM)
TRIG = 17
ECHO = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # Phát xung trigger 10us
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Đo thời gian ECHO lên cao
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # Tính khoảng cách (tốc độ âm thanh = 34300 cm/s)
    elapsed = stop_time - start_time
    dist = (elapsed * 34300) / 2
    return dist

try:
    while True:
        d = distance()
        print("Khoảng cách = %.1f cm" % d)
        time.sleep(1)

except KeyboardInterrupt:
    print("Dừng đo")
    GPIO.cleanup()
