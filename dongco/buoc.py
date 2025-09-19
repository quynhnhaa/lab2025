import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26

control_pins = [IN1, IN2, IN3, IN4]

STEPS_PER_REV = 532  # số half-steps cho 360 độ


for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Chuỗi bước nửa bước (half-step) cho 28BYJ-48
halfstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

def step_motor(steps, delay=0.001):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    for _ in range(steps):
        for step in range(8)[::direction]:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[step][pin])
            time.sleep(delay)

def rotate_degree(degree, delay=0.001):
    steps = int(degree * STEPS_PER_REV / 360)
    step_motor(steps, delay)

try:
    while True:
        print("Quay thuận 524 bước (360 độ)")
        rotate_degree(90)
        time.sleep(1)

        print("Quay ngược 262 bước (180 độ)")
        rotate_degree(-45)
        time.sleep(1)



except KeyboardInterrupt:
    print("Dừng bởi người dùng")
    print("Dừng động cơ")
    for pin in control_pins:
        GPIO.output(pin, 0)

finally:
    GPIO.cleanup()
