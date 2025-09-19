import RPi.GPIO as GPIO
import time

SENSOR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(SENSOR_PIN) == 0:
            print("Có vật cản")
        else:
            print("Không có vật cản")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
