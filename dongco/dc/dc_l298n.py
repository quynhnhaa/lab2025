import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Tắt cảnh báo GPIO

# Khai báo chân kết nối với module L298N
ENA = 17  # Chân Enable A (điều khiển tốc độ động cơ A)
IN1 = 27  # Chân Input 1 cho động cơ A
IN2 = 22  # Chân Input 2 cho động cơ A

# Thiết lập chân là output
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Tạo đối tượng PWM trên chân ENA với tần số 100Hz (thích hợp cho động cơ DC)
pwm = GPIO.PWM(ENA, 100)
pwm.start(0)  # Bắt đầu với duty cycle = 0 (tốc độ 0)

def forward(speed):
    """
    Quay động cơ theo chiều thuận với tốc độ được chỉ định.
    :param speed: Tốc độ từ 0 (dừng) đến 100 (tối đa).
    """
    if speed < 0:
        speed = 0
    elif speed > 100:
        speed = 100
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)
    print(f"Động cơ quay thuận với tốc độ {speed}%")

def backward(speed):
    """
    Quay động cơ theo chiều ngược với tốc độ được chỉ định.
    :param speed: Tốc độ từ 0 (dừng) đến 100 (tối đa).
    """
    if speed < 0:
        speed = 0
    elif speed > 100:
        speed = 100
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)
    print(f"Động cơ quay ngược với tốc độ {speed}%")

def stop():
    """
    Dừng động cơ.
    """
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    print("Động cơ dừng")

def cleanup():
    """
    Dọn dẹp GPIO trước khi thoát chương trình.
    """
    pwm.stop()
    GPIO.cleanup()
    print("Đã dọn dẹp GPIO")

if __name__ == "__main__":
    try:
        print("Chương trình điều khiển động cơ DC với module L298N")
        print("Nhấn Ctrl+C để dừng")

        while True:
            # Quay thuận với tốc độ chậm (50%)
            forward(50)
            time.sleep(3)

            # Dừng động cơ
            stop()
            time.sleep(1)

            # Quay thuận với tốc độ nhanh (100%)
            forward(100)
            time.sleep(3)

            # Dừng động cơ
            stop()
            time.sleep(1)

            # Quay ngược với tốc độ chậm (50%)
            backward(50)
            time.sleep(3)

            # Dừng động cơ
            stop()
            time.sleep(1)

            # Quay ngược với tốc độ nhanh (100%)
            backward(100)
            time.sleep(3)

            # Dừng động cơ
            stop()
            time.sleep(2)  # Nghỉ lâu hơn để lặp lại

    except KeyboardInterrupt:
        print("\nĐã nhấn Ctrl+C, dừng chương trình")
    finally:
        cleanup()