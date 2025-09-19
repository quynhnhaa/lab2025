
import time
import RPi.GPIO as GPIO

def main():
    global last_distance
    GPIO.setmode(GPIO.BOARD)

    TRIG_PIN = 17
    ECHO_PIN = 27

    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    pulse_start_time = 0
    pulse_end_time = 0

    while True:

        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(2E-6)
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(10E-6)
        GPIO.output(TRIG_PIN, GPIO.LOW)

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start_time = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        if distance > 300 or distance <= 0:
            distance = last_distance
        else:
            last_distance = distance
        
        print(distance)
        time.sleep(1)

main()