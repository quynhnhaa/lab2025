import Adafruit_DHT
import time

# Chọn loại cảm biến: DHT11 hoặc DHT22
SENSOR = Adafruit_DHT.DHT11
PIN = 4  # GPIO4 (chân số 7 trên Pi header)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is not None and temperature is not None:
        print("Nhiệt độ = {:.1f}°C  Độ ẩm = {:.1f}%".format(temperature, humidity))
    else:
        print("Không đọc được dữ liệu")
    time.sleep(2)
