import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # Phát xung trigger 10us
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = start_time

    # Chờ ECHO lên cao (timeout 0.02s)
    timeout = start_time + 0.02
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start_time = time.time()

    # Chờ ECHO xuống thấp (timeout 0.02s)
    timeout = time.time() + 0.02
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        stop_time = time.time()

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
