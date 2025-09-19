import RPi.GPIO as GPIO
import time
trig = 17
echo = 27

GPIO.setmode (GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
def distance():
    GPIO.output (trig, False)
    time.sleep(0.01)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    pulse_start = pulse_end = 0
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    dist = duration * 34300 / 2
    return dist

try:
    print("Hello")
    while True:
        d = distance()
        print("Distance:", d, "cm")

        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
print("Hello")