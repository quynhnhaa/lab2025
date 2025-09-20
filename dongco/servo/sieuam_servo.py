import RPi.GPIO as GPIO
import time


SERVO_PIN = 18 # chân số 6 bên phải

TRIG = 17 # chân số 6 bên trái  
ECHO = 27 # chân số 7 bên trái
TIMEOUT = 0.1

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Tạo đối tượng PWM với tần số 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50) 
pwm.start(0) 
def set_angle(angle):
    """
    Hàm này chuyển đổi góc (0-180) thành duty cycle (2-12) và đặt vị trí cho servo.
    
    - Góc 0   độ tương ứng với duty cycle ~2% (xung 1ms trên chu kỳ 20ms)
    - Góc 90  độ tương ứng với duty cycle ~7% (xung 1.5ms)
    - Góc 180 độ tương ứng với duty cycle ~12% (xung 2ms)
    """
    if angle < 0 or angle > 180:
        print("Góc phải nằm trong khoảng từ 0 đến 180 độ.")
        return
        
    duty_cycle = (angle / 18.0) + 2

    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

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
                set_angle(90)
                time.sleep(0.5)
                set_angle(0)
            elif 10 <= d <= 20:
                set_angle(180)
                time.sleep(0.5)
                set_angle(0)
            else:
                set_angle(0)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nĐang dọn dẹp và thoát chương trình...")

    finally:
        pwm.stop()
        GPIO.cleanup()
        print("Đã dọn dẹp GPIO")
