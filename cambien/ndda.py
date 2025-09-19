import time
import board
import adafruit_dht

# Chọn loại DHT: DHT11 hoặc DHT22
dhtDevice = adafruit_dht.DHT22(board.D4)  # GPIO4 (chân số 7)

while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if humidity is not None and temperature_c is not None:
            print("Nhiệt độ = {:.1f}°C  Độ ẩm = {:.1f}%".format(temperature_c, humidity))
        else:
            print("Không đọc được dữ liệu")
    except RuntimeError as error:
        # Thư viện này hay bị lỗi đọc tạm thời
        print(error.args[0])
    time.sleep(2)
