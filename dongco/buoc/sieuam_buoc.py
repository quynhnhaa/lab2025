import RPi.GPIO as GPIO
import time

control_pins = [6, 13, 19, 26]  # IN1, IN2, IN3, IN4 (lần lượt là 4 chân gần cuối bên trái)
STEPS_PER_REV = 532  # số half-steps cho 360 độ

TRIG = 17 # (chân số 6 bên trái)  
ECHO = 18 # (chân số 6 bên phải)
TIMEOUT = 0.1

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

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


def distance():
    GPIO.output(TRIG, False)


    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    
    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        # Kiểm tra timeout
        if start_time - timeout_start > TIMEOUT:
            print("Lỗi: Timeout khi chờ ECHO lên cao")
            return -1  

    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        # Kiểm tra timeout
        if stop_time - timeout_start > TIMEOUT:
            print("Lỗi: Timeout khi chờ ECHO xuống thấp")
            return -1 

    
    elapsed = stop_time - start_time
    dist = (elapsed * 34300) / 2
    
    return dist


if __name__ == "__main__":
    try:
        while True:
            d = distance()
            print("Khoảng cách = %.1f cm" % d)
            if d < 10:
                # print("Quay thuận 90 độ")
                rotate_degree(-90)
            elif 10 <= d <= 20:
                # print("Quay ngược 60 độ")
                rotate_degree(60)
            else:
                rotate_degree(0)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Dừng động cơ")
        for pin in control_pins:
            GPIO.output(pin, 0)

    finally:
        GPIO.cleanup()
