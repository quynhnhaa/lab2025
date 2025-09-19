import time
import RPi.GPIO as GPIO

# Khai báo sử dụng cách đánh dấu PIN theo BCM
GPIO.setmode(GPIO.BCM)

# Khởi tạo 2 biến chứa GPIO ta sử dụng
GPIO_TRIGGER = 23
GPIO_ECHO = 24

print("Ultrasonic Measurement - Press Ctrl+C to exit")

# Thiết lập GPIO nào để gửi tín hiệu và nhận tín hiệu
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Đảm bảo Trigger ở mức thấp ban đầu
GPIO.output(GPIO_TRIGGER, False)

# Đợi một chút để cảm biến ổn định
time.sleep(0.5)

try:
    while True:
        # Kích hoạt cảm biến bằng cách gửi một xung ngắn
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        # Khởi tạo biến thời gian để tránh lỗi
        start = time.time()
        stop = time.time()

        # Đợi tín hiệu Echo bắt đầu (pin chuyển sang HIGH)
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()

        # Đợi tín hiệu Echo kết thúc (pin chuyển về LOW)
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()

        # Tính toán thời gian của xung tín hiệu
        elapsed = stop - start

        # Tính khoảng cách
        distance = (elapsed * 34000) / 2

        print("Distance : %.1f cm" % distance)
        
        # Đợi 1 giây cho lần đo tiếp theo
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMeasurement stopped by user.")

finally:
    # Reset GPIO settings
    GPIO.cleanup()