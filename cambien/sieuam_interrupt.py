import RPi.GPIO as GPIO
import time

# ---------- PIN CONFIGURATION ----------
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# ---- Global variables for callbacks ----
# Các biến toàn cục để lưu trữ giá trị thời gian từ các hàm callback
pulse_start_time = 0
pulse_end_time = 0

def echo_callback(channel):
    """Hàm này được tự động gọi mỗi khi chân ECHO thay đổi trạng thái."""
    global pulse_start_time, pulse_end_time
    
    if GPIO.input(channel):  # Nếu pin chuyển sang HIGH, đó là lúc xung bắt đầu
        pulse_start_time = time.time()
    else:  # Nếu pin chuyển sang LOW, đó là lúc xung kết thúc
        pulse_end_time = time.time()

# ---------- SETUP ----------
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Thêm bộ phát hiện sự kiện. Hàm echo_callback sẽ được gọi trên cả hai sườn (lên và xuống).
GPIO.add_event_detect(GPIO_ECHO, GPIO.BOTH, callback=echo_callback)

print("Đo khoảng cách bằng Interrupt... Nhấn Ctrl+C để thoát.")

try:
    while True:
        # Reset các biến thời gian trước mỗi lần đo mới
        pulse_start_time = 0
        pulse_end_time = 0

        # Kích hoạt cảm biến để nó phát ra xung siêu âm
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        # Đợi một chút để các hàm callback chạy ở nền và cập nhật giá trị
        # Thêm một timeout ngắn để tránh bị kẹt nếu không nhận được tín hiệu phản hồi
        timeout_start = time.time()
        while pulse_end_time == 0:
            if time.time() - timeout_start > 0.2:  # Timeout 200ms
                break  # Thoát khỏi vòng lặp chờ

        # Sau khi chờ, kiểm tra xem có nhận được kết quả hợp lệ không
        if pulse_start_time != 0 and pulse_end_time != 0 and pulse_end_time > pulse_start_time:
            pulse_duration = pulse_end_time - pulse_start_time
            # Tốc độ âm thanh là ~34300 cm/s
            distance = (pulse_duration * 34300) / 2
            print(f"Khoảng cách: {distance:.1f} cm")
        else:
            print("Không đo được (timeout hoặc tín hiệu lỗi).")

        # Đợi 1 giây cho lần đo tiếp theo
        time.sleep(1)

except KeyboardInterrupt:
    print("\nChương trình bị dừng.")

finally:
    GPIO.cleanup()
    print("Đã dọn dẹp GPIO.")
