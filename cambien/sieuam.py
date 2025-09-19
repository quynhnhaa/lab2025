# import RPi.GPIO as GPIO
# import time

# # Gán chân GPIO (theo BCM)
# TRIG = 17 #(chân số 6 bên trái)  
# ECHO = 18 #(chân số 6 bên phải)

# TIMEOUT = 0.1

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)

# def distance():
#     GPIO.output(TRIG, False)


#     GPIO.output(TRIG, True)
#     time.sleep(0.00001)
#     GPIO.output(TRIG, False)

#     start_time = time.time()
#     stop_time = time.time()

    
#     timeout_start = time.time()
#     while GPIO.input(ECHO) == 0:
#         start_time = time.time()
#         # Kiểm tra timeout
#         if start_time - timeout_start > TIMEOUT:
#             print("Lỗi: Timeout khi chờ ECHO lên cao")
#             return -1  

#     timeout_start = time.time()
#     while GPIO.input(ECHO) == 1:
#         stop_time = time.time()
#         # Kiểm tra timeout
#         if stop_time - timeout_start > TIMEOUT:
#             print("Lỗi: Timeout khi chờ ECHO xuống thấp")
#             return -1 

    
#     elapsed = stop_time - start_time
#     dist = (elapsed * 34300) / 2
    
#     if dist < 2 or dist > 400:
#         return -1  # Trả về giá trị lỗi nếu ngoài phạm vi
    
#     return dist

# try:
#     while True:
#         d = distance()
#         if d > 0:
#             print("Khoảng cách = %.1f cm" % d)
#         else:
#             print("Lỗi đo khoảng cách")
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("Dừng đo")
#     GPIO.cleanup()

import RPi.GPIO as GPIO
import time

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
