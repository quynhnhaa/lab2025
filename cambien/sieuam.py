import RPi.GPIO as GPIO
import time

# Gán chân GPIO (theo BCM)
TRIG = 23 #(chân số 6 bên trái)  
ECHO = 24 #(chân số 6 bên phải)

TIMEOUT = 0.1

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

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
    
    if dist < 2 or dist > 400:
        return -1  # Trả về giá trị lỗi nếu ngoài phạm vi
    
    return dist

try:
    while True:
        d = distance()
        if d > 0:
            print("Khoảng cách = %.1f cm" % d)
        else:
            print("Lỗi đo khoảng cách")
        time.sleep(1)

except KeyboardInterrupt:
    print("Dừng đo")
    GPIO.cleanup()