import RPi.GPIO as GPIO
import time


TRIG_PIN = 17
ECHO_PIN = 18
pulse_start_time = pulse_start_end = 0
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    print("Thiết lập cảm biến siêu âm hoàn tất.")

def get_distance():
    """Đo khoảng cách bằng cảm biến siêu âm."""
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.2)

    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Ghi lại thời điểm khi chân ECHO chuyển sang HIGH
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()

    # Ghi lại thời điểm khi chân ECHO chuyển về LOW
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300) / 2

    return distance

def main():
    """Vòng lặp chính để liên tục đo và in khoảng cách."""
    try:
        setup()
        while True:
            dist = get_distance()
            print(f"Khoảng cách: {dist:.2f} cm")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nĐo lường bị dừng bởi người dùng.")
    finally:
        GPIO.cleanup()
        print("Đã dọn dẹp GPIO. Thoát chương trình.")

if __name__ == '__main__':
    main()
