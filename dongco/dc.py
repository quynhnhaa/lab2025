# dc_motor_control.py

import RPi.GPIO as GPIO
import time


ENA = 25  # Chân Enable A (điều khiển tốc độ)
IN1 = 24  # Chân Input 1
IN2 = 23  # Chân Input 2

# Thiết lập chế độ chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Tạo đối tượng PWM trên chân ENA với tần số 100Hz
# Tần số cao hơn giúp động cơ chạy mượt hơn
speed_pwm = GPIO.PWM(ENA, 100)
speed_pwm.start(0) # Bắt đầu với tốc độ 0

def set_speed(speed):
    """
    Hàm đặt tốc độ động cơ.
    :param speed: Tốc độ từ 0 (dừng) đến 100 (tối đa).
    """
    if speed < 0:
        speed = 0
    elif speed > 100:
        speed = 100
    print(f"Đặt tốc độ: {speed}%")
    speed_pwm.ChangeDutyCycle(speed)

def forward():
    """động cơ quay thuận."""
    print("Động cơ quay thuận...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def backward():
    """động cơ quay ngược."""
    print("Động cơ quay ngược...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def stop():
    """Dừng động cơ."""
    print("Dừng động cơ.")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    set_speed(0) # Đặt tốc độ về 0

def cleanup():
    """Dọn dẹp GPIO trước khi thoát."""
    print("Dọn dẹp GPIO và thoát...")
    speed_pwm.stop()
    GPIO.cleanup()

# --- Chương trình chính ---
if __name__ == "__main__":
    try:
        print("Chương trình điều khiển động cơ DC.")
        print("Bắt đầu chuỗi hành động tự động. Nhấn Ctrl+C để thoát.")

        SLOW_SPEED = 30
        FAST_SPEED = 60

        while True:
            # 1. Quay thuận, tốc độ chậm
            set_speed(SLOW_SPEED)
            forward()
            time.sleep(2) # Quay trong 2 giây
            stop()
            time.sleep(1)
            
            # 2. Quay thuận, tốc độ nhanh
            set_speed(FAST_SPEED)
            forward()
            time.sleep(2)
            stop()
            time.sleep(1)
            
            # 3. Quay ngược, tốc độ chậm và nhanh (tương tự)
            print("--- Đổi chiều ---")
            set_speed(SLOW_SPEED)
            backward()
            time.sleep(2)
            stop()
            time.sleep(1)
            
            set_speed(FAST_SPEED)
            backward()
            time.sleep(2)
            stop()
            time.sleep(1)


    except KeyboardInterrupt:
        print("\nĐã nhấn Ctrl+C.")
    finally:
        cleanup()
