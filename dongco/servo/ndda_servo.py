import RPi.GPIO as GPIO
import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO4 (chân số 4 bên trái)

SERVO_PIN = 18 # chân số 6 bên phải

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Tạo đối tượng PWM với tần số 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50) 
pwm.start(0) 
def set_angle(angle):
    """
    Hàm này chuyển đổi góc (0-180) thành duty cycle (2-12) và đặt vị trí cho servo.
    
    - Góc 0   độ tương ứng với duty cycle ~2% (xung 1ms trên chu kỳ 20ms)
    - Góc 90  độ tương ứng với duty cycle ~7% (xung 1.5ms)
    - Góc 180 độ tương ứng với duty cycle ~12% (xung 2ms)
    """
    if angle < 0 or angle > 180:
        print("Góc phải nằm trong khoảng từ 0 đến 180 độ.")
        return
        
    duty_cycle = (angle / 18.0) + 2

    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

if __name__ == "__main__":
    try:
        while True:
            try:
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity
                if humidity is not None and temperature_c is not None:
                    print("Nhiệt độ = {:.1f}°C  Độ ẩm = {:.1f}%".format(temperature_c, humidity))

                    if temperature_c >= 75:
                        set_angle(180)
                        time.sleep(0.5)
                        set_angle(0)
                    else:
                        set_angle(90)
                        time.sleep(0.5)
                        set_angle(0)
                else:
                    print("Không đọc được dữ liệu")
                time.sleep(0.5)
            except RuntimeError as error:
                # Thư viện này hay bị lỗi đọc tạm thời
                print(error.args[0])

    except KeyboardInterrupt:
        print("\nĐang dọn dẹp và thoát chương trình...")

    finally:
        pwm.stop()
        GPIO.cleanup()
