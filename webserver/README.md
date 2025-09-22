# Dự án IoT Raspberry với Webserver

## Giới thiệu
Dự án này sử dụng Raspberry Pi để giám sát nhiệt độ và độ ẩm thông qua cảm biến DHT11, đồng thời điều khiển 4 đèn LED với nhiều chế độ khác nhau. Webserver Flask cung cấp giao diện web để hiển thị dữ liệu cảm biến và chuyển đổi chế độ hoạt động của LED.

## Các file chính

### 1. `main.py`
- Chạy webserver Flask trên Raspberry Pi.
- Đọc dữ liệu từ cảm biến DHT11 (nhiệt độ, độ ẩm).
- Điều khiển 4 đèn LED với các chế độ:
	- **Auto**: Tự động bật/tắt LED dựa vào ngưỡng độ ẩm.
	- **Mode 1**: LED sáng tuần tự từ trái sang phải và ngược lại.
	- **Mode 2**: LED sáng dần và tắt dần từng cái một.
- Cung cấp API để lấy dữ liệu cảm biến và chuyển đổi chế độ LED.

### 2. `html.html`
- Giao diện web hiển thị nhiệt độ, độ ẩm và trạng thái chế độ LED.
- Có các nút để chuyển đổi chế độ hoạt động của LED.
- Tự động cập nhật dữ liệu cảm biến mỗi giây.

## Yêu cầu cài đặt

### Phần cứng
- Raspberry Pi (đã cài đặt hệ điều hành Raspbian hoặc tương tự)
- Cảm biến DHT11
- 4 đèn LED và điện trở
- Dây nối GPIO

### Phần mềm
- Python 3
- Các thư viện Python:
	- Flask
	- RPi.GPIO
	- adafruit-circuitpython-dht
	- board

Cài đặt các thư viện bằng lệnh:
```bash
pip install flask RPi.GPIO adafruit-circuitpython-dht board
```

## Hướng dẫn sử dụng
1. Kết nối phần cứng theo sơ đồ GPIO trong mã nguồn.
2. Chạy file `main.py`:
	 ```bash
	 python3 main.py
	 ```
3. Truy cập địa chỉ web: `http://<IP_Raspberry>:5000` trên trình duyệt để xem giao diện và điều khiển LED.