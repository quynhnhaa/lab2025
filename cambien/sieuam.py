import RPi.GPIO as GPIO
import time

# ---------- PIN CONFIGURATION ----------
# Bạn có thể thay đổi các chân GPIO này cho phù hợp với cách nối dây của bạn.
TRIG_PIN = 17
ECHO_PIN = 18

def setup():
    """Thiết lập các chân GPIO."""
    # Sử dụng chế độ đánh số chân BCM (Broadcom)
    GPIO.setmode(GPIO.BCM)
    # Thiết lập chân TRIG là OUTPUT (để gửi tín hiệu)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    # Thiết lập chân ECHO là INPUT (để nhận tín hiệu)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    print("Thiết lập cảm biến siêu âm hoàn tất.")

def get_distance():
    """Đo khoảng cách bằng cảm biến siêu âm (phiên bản đã sửa lỗi)."""
    # Đảm bảo chân TRIG ở mức thấp ban đầu
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.1) # Đợi một chút để ổn định

    # Gửi một xung 10 micro-giây để kích hoạt cảm biến
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Khởi tạo biến thời gian để tránh lỗi UnboundLocalError
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    # Chờ chân ECHO chuyển sang HIGH, ghi lại thời gian bắt đầu
    # Thêm timeout để tránh vòng lặp vô hạn
    timeout_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()
        if time.time() - timeout_start > 1:
            print("Lỗi: Timeout khi chờ tín hiệu ECHO bắt đầu.")
            return -1 # Trả về giá trị lỗi

    # Chờ chân ECHO chuyển về LOW, ghi lại thời gian kết thúc
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()
        # Timeout này kiểm tra thời gian của tín hiệu phản hồi
        if (pulse_end_time - pulse_start_time) > 1:
            print("Lỗi: Tín hiệu ECHO kéo dài bất thường.")
            return -1 # Trả về giá trị lỗi

    # Tính toán thời gian và khoảng cách
    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300) / 2

    return distance

def main():
    """Vòng lặp chính để liên tục đo và in khoảng cách."""
    try:
        setup()
        while True:
            dist = get_distance()
            if dist != -1: # Chỉ in khoảng cách hợp lệ
                print(f"Khoảng cách: {dist:.2f} cm")
            time.sleep(1)

    except KeyboardInterrupt:
        # Xử lý khi người dùng nhấn Ctrl+C
        print("\nĐo lường bị dừng bởi người dùng.")
    finally:
        # Dọn dẹp các thiết lập GPIO trước khi thoát
        GPIO.cleanup()
        print("Đã dọn dẹp GPIO. Thoát chương trình.")

if __name__ == '__main__':
    main()