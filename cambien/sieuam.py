import RPi.GPIO as GPIO
import time

# ---------- PIN CONFIGURATION ----------
TRIG_PIN = 17
ECHO_PIN = 27
last_distance = 0

# ---------- GPIO SETUP ----------

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

pulse_start_time = 0
pulse_end_time = 0
print("Bắt đầu đo... Nhấn Ctrl+C để thoát.")

try:
    # Vòng lặp chính của chương trình
    while True:

        # --- Gửi xung trigger ---
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(2E-6) # 2 micro-giây
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(10E-6) # 10 micro-giây
        GPIO.output(TRIG_PIN, GPIO.LOW)

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start_time = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end_time = time.time()

        # --- Tính toán và lọc khoảng cách ---
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        
        if distance > 300 or distance <= 0:
            distance = last_distance
        else:
            last_distance = distance
        
        print(f"Khoảng cách: {distance:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nChương trình bị dừng bởi người dùng.")

finally:
    # Dọn dẹp các thiết lập GPIO trước khi thoát
    GPIO.cleanup()
    print("Đã dọn dẹp GPIO.")
