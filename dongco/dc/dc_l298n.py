import pigpio
from time import sleep

# --- Khai báo chân ---
ENA = 17   # PWM
IN1 = 27   # Điều khiển chiều
IN2 = 22   # Điều khiển chiều

# --- Khởi tạo pigpio ---
pi = pigpio.pi()
if not pi.connected:
    exit("Không kết nối được pigpio daemon. Hãy chạy: sudo systemctl start pigpiod")

# Đặt mode cho các chân
pi.set_mode(ENA, pigpio.OUTPUT)
pi.set_mode(IN1, pigpio.OUTPUT)
pi.set_mode(IN2, pigpio.OUTPUT)

# Đặt tần số PWM cho ENA (ví dụ 1kHz)
pi.set_PWM_frequency(ENA, 1000)

def forward(speed):
    """Quay thuận với tốc độ (0-100%)"""
    pi.write(IN1, 1)
    pi.write(IN2, 0)
    pi.set_PWM_dutycycle(ENA, int(speed * 255 / 100))  # scale 0-100 → 0-255

def backward(speed):
    """Quay ngược với tốc độ (0-100%)"""
    pi.write(IN1, 0)
    pi.write(IN2, 1)
    pi.set_PWM_dutycycle(ENA, int(speed * 255 / 100))

def stop():
    """Dừng motor"""
    pi.set_PWM_dutycycle(ENA, 0)
    pi.write(IN1, 0)
    pi.write(IN2, 0)

try:
    while True:
        print("Quay thuận chậm (30%)")
        forward(30)
        sleep(2)

        print("Tăng tốc (70%)")
        forward(70)
        sleep(2)

        print("Dừng 1s")
        stop()
        sleep(1)

        print("Quay ngược nhanh (80%)")
        backward(80)
        sleep(2)

        print("Quay ngược chậm (40%)")
        backward(40)
        sleep(2)

        print("Dừng 1s")
        stop()
        sleep(1)

except KeyboardInterrupt:
    print("Kết thúc bởi người dùng")
finally:
    stop()
    pi.stop()
