import RPi.GPIO as GPIO
import time
import board
import adafruit_dht

GPIO.setmode(GPIO.BCM)

control_pins = [6, 13, 19, 26]  # IN1, IN2, IN3, IN4 (lần lượt là 4 chân gần cuối bên trái)
STEPS_PER_REV = 532  # số half-steps cho 360 độ


dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO4 (chân số 4 bên trái)

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Chuỗi bước nửa bước (half-step) cho 28BYJ-48
halfstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

def step_motor(steps, delay=0.001):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    for _ in range(steps):
        for step in range(8)[::direction]:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[step][pin])
            time.sleep(delay)

def rotate_degree(degree, delay=0.001):
    steps = int(degree * STEPS_PER_REV / 360)
    step_motor(steps, delay)

if __name__ == "__main__":
    try:
        while True:
            try:
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity
                if humidity is not None and temperature_c is not None:
                    print("Nhiệt độ = {:.1f}°C  Độ ẩm = {:.1f}%".format(temperature_c, humidity))
                    if humidity > 80:
                        print("Quay ngược 90 độ")
                        rotate_degree(-90)
                    else:
                        print("Quay thuận 90 độ")
                        rotate_degree(90)

                else:
                    print("Không đọc được dữ liệu")
                time.sleep(1)
            except RuntimeError as error:
                # Thư viện này hay bị lỗi đọc tạm thời
                print(error.args[0])

    except KeyboardInterrupt:
        for pin in control_pins:
            GPIO.output(pin, 0)
    finally:
        GPIO.cleanup()
