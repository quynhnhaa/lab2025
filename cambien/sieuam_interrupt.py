import pigpio
import time

TRIG = 23
ECHO = 24

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Không kết nối được pigpio daemon")

pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)

def get_distance():
    # phát xung
    pi.write(TRIG, 0)
    time.sleep(0.00002)  # đảm bảo chân TRIG thấp trước
    pi.write(TRIG, 1)
    time.sleep(0.00001)
    pi.write(TRIG, 0)

    # đo thời gian chân ECHO HIGH
    pulse_length = pi.wait_for_edge(ECHO, pigpio.RISING_EDGE, timeout=1000000)  # nghĩa là đợi cạnh lên
    if pulse_length < 0:
        return None
    t1 = time.time()
    pulse_length2 = pi.wait_for_edge(ECHO, pigpio.FALLING_EDGE, timeout=1000000)
    if pulse_length2 < 0:
        return None
    t2 = time.time()

    # khoảng thời gian cao là t2 - t1
    elapsed = t2 - t1
    distance_cm = (elapsed * 34300) / 2
    return distance_cm

try:
    while True:
        d = get_distance()
        if d is not None:
            print("Khoảng cách: {:.1f} cm".format(d))
        else:
            print("Không đo được")
        time.sleep(0.5)
finally:
    pi.stop()
