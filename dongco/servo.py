import RPi.GPIO as GPIO
import time


SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Tạo đối tượng PWM với tần số 50Hz
# Tần số 50Hz là tiêu chuẩn cho hầu hết các servo analog
pwm = GPIO.PWM(SERVO_PIN, 50) 
pwm.start(0) # Bắt đầu PWM với duty cycle là 0 (servo không di chuyển)

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
    
    # Thay đổi duty cycle để di chuyển servo
    # Tham số 0 có nghĩa là không có độ trễ, servo sẽ di chuyển ngay lập tức
    pwm.ChangeDutyCycle(duty_cycle)
    
    # Đợi một chút để servo có thời gian di chuyển đến vị trí mới
    time.sleep(0.5)
    
    # Tắt tín hiệu PWM để giảm rung và tiết kiệm năng lượng
    # Servo sẽ giữ nguyên vị trí cuối cùng
    pwm.ChangeDutyCycle(0)

try:
    print("Điều khiển Servo")
    
    print("Di chuyển servo đến góc 90 độ...")
    set_angle(90)
    time.sleep(1) 
    
    
    print("Quay servo trở lại góc 0 độ...")
    set_angle(0)
    time.sleep(1) 
    

except KeyboardInterrupt:
    print("\nĐang dọn dẹp và thoát chương trình...")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("Đã dọn dẹp GPIO. Tạm biệt!")
