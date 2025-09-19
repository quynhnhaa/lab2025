import RPi.GPIO as GPIO
import time

# ---------- PIN CONFIGURATION ----------
TRIG_PIN = 17
ECHO_PIN = 18
last_distance = 0  # Biến toàn cục để lưu khoảng cách hợp lệ cuối cùng

def setup():
    """Thiết lập các chân GPIO."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    print("Thiết lập cảm biến siêu âm hoàn tất.")

def get_distance():
    """Đo khoảng cách bằng cảm biến siêu âm theo logic bạn cung cấp."""
    global last_distance
    
    try:
        pulse_start_time = 0
        pulse_end_time = 0

        # Tạo một xung trigger ngắn
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(2E-6)  # 2 micro-giây
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(10E-6) # 10 micro-giây
        GPIO.output(TRIG_PIN, GPIO.LOW)

        # Đợi cho đến khi chân ECHO lên mức HIGH
        # Lưu ý: Vòng lặp này có thể bị treo nếu cảm biến không hoạt động
        while GPIO.input(ECHO_PIN) == 0:
            pass
        pulse_start_time = time.time()

        # Đợi cho đến khi chân ECHO xuống mức LOW
        while GPIO.input(ECHO_PIN) == 1:
            pass
        pulse_end_time = time.time()

        # Tính toán khoảng cách
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        return distance
        
    except Exception as e:
        print(f"Lỗi trong hàm get_distance: {e}")
        return last_distance

def main():
    """Vòng lặp chính để liên tục đo và in khoảng cách."""
    try:
        setup()
        while True:
            dist = get_distance()
            print(f"Khoảng cách: {dist:.2f} cm")
            # time.sleep(1)

    except KeyboardInterrupt:
        print("\nĐo lường bị dừng bởi người dùng.")
    finally:
        GPIO.cleanup()
        print("Đã dọn dẹp GPIO. Thoát chương trình.")

if __name__ == '__main__':
    main()
