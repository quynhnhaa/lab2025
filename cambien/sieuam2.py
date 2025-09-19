import RPi.GPIO as GPIO
import time

# Gán chân GPIO (theo BCM)
TRIG = 23
ECHO = 24

# Thời gian timeout (giây) - ví dụ: chờ tối đa 0.1 giây
TIMEOUT = 0.1

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # Đảm bảo chân TRIG ở mức thấp ban đầu
    GPIO.output(TRIG, False)
    time.sleep(0.01)  # Ổn định cảm biến

    # Phát xung trigger 10us
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    # Đo thời gian ECHO lên cao với timeout
    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        # Kiểm tra timeout
        if start_time - timeout_start > TIMEOUT:
            print("Lỗi: Timeout khi chờ ECHO lên cao")
            return -1  # Trả về giá trị lỗi

    # Đo thời gian ECHO xuống thấp với timeout
    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        # Kiểm tra timeout
        if stop_time - timeout_start > TIMEOUT:
            print("Lỗi: Timeout khi chờ ECHO xuống thấp")
            return -1  # Trả về giá trị lỗi

    # Tính khoảng cách (tốc độ âm thanh = 34300 cm/s)
    elapsed = stop_time - start_time
    dist = (elapsed * 34300) / 2
    
    # Kiểm tra khoảng cách hợp lệ (ví dụ: trong phạm vi 2-400cm)
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