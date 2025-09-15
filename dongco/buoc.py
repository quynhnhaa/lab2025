# /Users/quynhnhaa/Documents/Ahn/Study/Year4.1/IoT/lab2025/dongco/buoc.py
import RPi.GPIO as GPIO
import time
import math

# BCM pins -> chỉnh theo dây của bạn vào ULN2003 IN1..IN4
IN1, IN2, IN3, IN4 = 17, 18, 27, 22

# Half-step sequence (mượt, mô-men tốt)
HALF_STEP_SEQ = [
    (1,0,0,0),
    (1,1,0,0),
    (0,1,0,0),
    (0,1,1,0),
    (0,0,1,0),
    (0,0,1,1),
    (0,0,0,1),
    (1,0,0,1),
]

# 28BYJ-48 ~ 4096 half-steps cho 360°
STEPS_PER_REV = 4096

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in (IN1, IN2, IN3, IN4):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def cleanup():
    for pin in (IN1, IN2, IN3, IN4):
        GPIO.output(pin, 0)
    GPIO.cleanup()

def step_once(seq_idx):
    a,b,c,d = HALF_STEP_SEQ[seq_idx]
    GPIO.output(IN1, a)
    GPIO.output(IN2, b)
    GPIO.output(IN3, c)
    GPIO.output(IN4, d)

def rotate_degrees(degrees, rpm=10, clockwise=True):
    # Tính tổng số bước cần đi
    steps_needed = int(STEPS_PER_REV * (abs(degrees) / 360.0))
    if steps_needed == 0:
        return

    # Tốc độ: rpm -> delay giữa các half-step
    # 1 vòng = STEPS_PER_REV steps -> thời gian 1 vòng = 60/rpm
    # delay mỗi step:
    delay = (60.0 / rpm) / STEPS_PER_REV
    delay = max(0.001, delay)  # giới hạn tối thiểu để ổn định

    seq_idx = 0
    direction = -1 if clockwise else 1

    for _ in range(steps_needed):
        step_once(seq_idx)
        time.sleep(delay)
        seq_idx = (seq_idx + direction) % len(HALF_STEP_SEQ)

def main():
    try:
        setup()
        print("Quay 90° theo chiều kim đồng hồ")
        rotate_degrees(90, rpm=12, clockwise=True)
        time.sleep(1)

        print("Quay 180° ngược chiều kim đồng hồ")
        rotate_degrees(180, rpm=12, clockwise=False)
        time.sleep(1)

        print("Hoàn tất")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
