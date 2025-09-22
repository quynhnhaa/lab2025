from flask import Flask, jsonify, render_template
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import threading

# --- GPIO setup ---

GPIO.setmode(GPIO.BCM)

SENSOR_PIN = 27 #(chân số 6 bên trái) 

GPIO.setup(SENSOR_PIN, GPIO.IN)

# --- DHT setup ---
SERVO_PIN = 14

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


# --- Flask ---
app = Flask(__name__, template_folder="templates")

# --- Global state ---
sensor_data = {"temperature": None, "humidity": None}
led_mode = 0
humidity_threshold = 60


# --- Sensor loop ---
def sensor_loop():
    global sensor_data
    while True:
        try:
            if GPIO.input(SENSOR_PIN) == 0:
                sensor_data["temperature"] = 'trắng'
            else:
                sensor_data["temperature"] = 'đen'
            

        except Exception as e:
            print("[SENSOR LOOP] Error:", e)
        time.sleep(1)


# --- LED loop ---
def led_loop():
    global led_mode, sensor_data
    while True:
        set_angle(int(led_mode))
        time.sleep(0.5) 
        set_angle(0)


# --- Routes ---
@app.route("/")
def index():
    return render_template("html.html")

@app.route("/api/sensor")
def get_sensor():
    return jsonify({
        "status": "success",
        "temperature": sensor_data.get("temperature"),
        "humidity": sensor_data.get("humidity"),
        "mode": led_mode
    })

from flask import request, jsonify

@app.route("/api/mode", methods=["POST"])
def change_mode():
    global led_mode
    data = request.get_json()  # lấy JSON từ frontend
    if not data or "mode" not in data:
        return jsonify({"status": "error", "message": "Missing 'mode'"}), 400

    led_mode = data["mode"]  # có thể là số hoặc chuỗi
    print(f"[API MODE] Mode changed to: {led_mode}")
    return jsonify({"status": "success", "mode": led_mode})

# --- Start threads ---
threading.Thread(target=sensor_loop, daemon=True).start()
threading.Thread(target=led_loop, daemon=True).start()

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
