# stepper_control.py

import RPi.GPIO as GPIO
import time

# Định nghĩa các chân GPIO kết nối với IN1, IN2, IN3, IN4 của ULN2003
STEPPER_PINS = [5, 6, 13, 19] # Theo thứ tự IN1, IN2, IN3, IN4

# Thiết lập chế độ chân GPIO
GPIO.setmode(GPIO.BCM)
for pin in STEPPER_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Trình tự cấp điện cho chế độ nửa bước (half-step), có 8 bước
HALF_STEP_SEQ = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# Trình tự ngược lại để quay ngược chiều
REVERSE_HALF_STEP_SEQ = HALF_STEP_SEQ[::-1]

def rotate(steps, direction='forward', delay=0.001):
    """
    Hàm quay động cơ một số bước nhất định.
    :param steps: Số bước cần quay.
    :param direction: Chiều quay ('forward' hoặc 'backward').
    :param delay: Thời gian nghỉ giữa các bước (càng nhỏ càng nhanh).
    """
    if direction == 'forward':
        sequence = HALF_STEP_SEQ
        print(f"Quay thuận {steps} bước...")
    else:
        sequence = REVERSE_HALF_STEP_SEQ
        print(f"Quay ngược {steps} bước...")

    step_counter = 0
    for _ in range(steps):
        for pin in range(4):
            GPIO.output(STEPPER_PINS[pin], sequence[step_counter][pin])
        
        step_counter = (step_counter + 1) % 8
        time.sleep(delay)

def cleanup():
    """Tắt nguồn các chân và dọn dẹp GPIO."""
    for pin in STEPPER_PINS:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

# --- Chương trình chính ---
if __name__ == "__main__":
    try:
        print("Chương trình điều khiển động cơ bước.")
        print("Nhấn Ctrl+C để thoát.")

        # Số bước cho 1 vòng quay là 4096
        # 90 độ ~ 1024 bước
        # 180 độ ~ 2048 bước
        steps_for_90_degrees = 1024
        steps_for_180_degrees = 2048

        while True:
            # Quay 90 độ thuận
            print("\n--- Quay 90 độ thuận ---")
            rotate(steps_for_90_degrees, direction='forward')
            time.sleep(1)

            # Quay 180 độ ngược
            print("\n--- Quay 180 độ ngược ---")
            rotate(steps_for_180_degrees, direction='backward')
            time.sleep(1)
            
            # Quay về vị trí ban đầu
            print("\n--- Quay 90 độ thuận về vị trí ban đầu ---")
            rotate(steps_for_90_degrees, direction='forward')
            time.sleep(2) # Nghỉ 2 giây trước khi lặp lại

    except KeyboardInterrupt:
        print("\nĐã nhấn Ctrl+C. Đang dọn dẹp...")
    finally:
        cleanup()
        print("Đã dọn dẹp GPIO. Tạm biệt!")