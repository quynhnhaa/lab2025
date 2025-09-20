import RPi.GPIO as GPIO
import time


SERVO_PIN = 18 # chân số 6 bên phải
SENSOR_PIN = 17 # chân số 6 bên trái

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)

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
if __name__ == "__main__":
    try:
        print("Điều khiển Servo")
        
        while True:
            if GPIO.input(SENSOR_PIN) == 0:
                print("Line trắng, servo quay góc 90 độ")
                set_angle(90)
                time.sleep(0.5)
                set_angle(0)
            else:
                print("Line đen, servo quay góc 180 độ")
                set_angle(180)
                time.sleep(0.5)
                set_angle(0)
                
            

    except KeyboardInterrupt:
        print("\nĐang dọn dẹp và thoát chương trình...")

    finally:
        pwm.stop()
        GPIO.cleanup()
        print("Đã dọn dẹp GPIO. Tạm biệt!")
