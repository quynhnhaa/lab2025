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
dhtDevice = adafruit_dht.DHT11(board.D4)

# --- Flask ---
app = Flask(__name__, template_folder="templates")

# --- Global state ---
sensor_data = {"temperature": None, "humidity": None}
led_mode = "auto"   # "auto", "mode1", "mode2"
humidity_threshold = 75


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
        if led_mode == "auto":
            hum = sensor_data.get("humidity")
            if hum is not None:
                if hum > humidity_threshold:
                    for pwm in pwms:
                        pwm.ChangeDutyCycle(100)
                else:
                    for pwm in pwms:
                        pwm.ChangeDutyCycle(0)
            time.sleep(0.5)

        elif led_mode == "mode1":
            # Left --> Right
            for pwm in pwms:
                pwm.ChangeDutyCycle(0)
            for i in range(len(pwms)):
                if led_mode != "mode1": break
                for j, pwm in enumerate(pwms):
                    pwm.ChangeDutyCycle(100 if j == i else 0)
                time.sleep(0.2)
            # Right --> Left
            for i in range(len(pwms)-2, 0, -1):
                if led_mode != "mode1": break
                for j, pwm in enumerate(pwms):
                    pwm.ChangeDutyCycle(100 if j == i else 0)
                time.sleep(0.2)

        elif led_mode == "mode2":
            # brighten
            for pwm in pwms:
                pwm.ChangeDutyCycle(0)
            for i in range(len(pwms)):
                if led_mode != "mode2": break
                for dc in range(0, 101, 5):
                    pwms[i].ChangeDutyCycle(dc)
                    time.sleep(0.05)
            # darkening
            for i in reversed(range(len(pwms))):
                if led_mode != "mode2": break
                for dc in reversed(range(0, 101, 5)):
                    pwms[i].ChangeDutyCycle(dc)
                    time.sleep(0.05)
        else:
            time.sleep(0.5)


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

@app.route("/api/mode/<mode>", methods=["POST"])
def change_mode(mode):
    global led_mode
    if mode in ["auto", "mode1", "mode2"]:
        led_mode = mode
        return jsonify({"status": "success", "mode": led_mode})
    return jsonify({"status": "error", "msg": "invalid mode"})


# --- Start threads ---
threading.Thread(target=sensor_loop, daemon=True).start()
threading.Thread(target=led_loop, daemon=True).start()

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
