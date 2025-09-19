import RPi.GPIO as GPIO
import time

SERVO = 18
TRIG  = 17
ECHO  = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(TRIG,  GPIO.OUT)
# Quan tr  ^mng: k  o xu  ^qng  ^q  ^c ECHO kh  ng b  ^k n  ^ui (floating)
GPIO.setup(ECHO,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pwm = GPIO.PWM(SERVO, 50)
pwm.start(0)

def set_angle(angle, settle=0.25):
    duty = 2.5 + (angle/180.0)*10.0
    pwm.ChangeDutyCycle(duty)
    time.sleep(settle)
    pwm.ChangeDutyCycle(0)

def distance_cm(max_wait_ms=40):
    #  ^q   m b   o ECHO  ^qang LOW tr    ^{c khi b   n xung
    if GPIO.input(ECHO) == 1:
        if GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=max_wait_ms) is None:
            return None, "echo_stuck_high"

    # ph  t xung TRIG 10us
    GPIO.output(TRIG, False); time.sleep(0.0002)
    GPIO.output(TRIG, True);  time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # ch  ^} c   nh l  n
    if GPIO.wait_for_edge(ECHO, GPIO.RISING, timeout=max_wait_ms) is None:
        return None, "no_rising"

    t1 = time.perf_counter()

    # ch  ^} c   nh xu  ^qng
    if GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=max_wait_ms) is None:
        return None, "no_falling"

    t2 = time.perf_counter()
    dur = t2 - t1
    dist = dur * 34300.0 / 2.0
    return dist, None
try:
    last_angle = None
    while True:
        d, err = distance_cm()
        if err:
            # debug ng   n g  ^mn, b  ^o n   u kh  ng c   n
            print("Distance error:", err, "ECHO=", GPIO.input(ECHO))
            time.sleep(0.1)
            continue

        print(f"Distance: {d:.1f} cm")

        if d < 10:
            set_angle(45); time.sleep(0.2)
            set_angle(0);  time.sleep(0.2)
            last_angle = 0
        elif 10 <= d <= 20:
            if last_angle != 90:
                set_angle(90)
                last_angle = 90
            time.sleep(0.1)
        else:
            #  ^q   ng y  n
            time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()