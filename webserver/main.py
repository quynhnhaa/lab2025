from flask import Flask, jsonify, render_template
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import threading

# --- GPIO setup ---
LED_PINS = [14, 15, 27, 22]  # 4 LED GPIO pins
GPIO.setmode(GPIO.BCM)
pwms = []
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 100)  # PWM 100Hz
    pwm.start(0)
    pwms.append(pwm)

# --- DHT setup ---
SERVO_PIN = 18

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


# --- Flask ---
app = Flask(__name__, template_folder="templates")

# --- Global state ---
sensor_data = {"temperature": None, "humidity": None}
led_mode = "auto"   # "auto", "mode1", "mode2"
humidity_threshold = 60


# --- Sensor loop ---
def sensor_loop():
    global sensor_data
    while True:
        try:
            temp = None
            hum = None
            for _ in range(3):
                try:
                    temp = dhtDevice.temperature
                    hum = dhtDevice.humidity
                    if temp is not None and hum is not None:
                        break
                except Exception:
                    time.sleep(0.2)
            sensor_data["temperature"] = temp
            sensor_data["humidity"] = hum
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

@app.route("/api/mode", methods=["POST"])
def change_mode(mode):
    global led_mode
    # if mode in ["auto", "mode1", "mode2"]:
    led_mode = mode['mode']
    return jsonify({"status": "success", "mode": led_mode})


# --- Start threads ---
threading.Thread(target=sensor_loop, daemon=True).start()
threading.Thread(target=led_loop, daemon=True).start()

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
