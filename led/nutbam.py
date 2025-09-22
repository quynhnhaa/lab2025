import gpiod
import threading
import time

CHIP = "gpiochip0"   # thường là /dev/gpiochip0
LINE_BTN = 17        # nút nhấn
LINE_LED = 27        # LED

chip = gpiod.Chip(CHIP)

# Lấy line cho nút
btn = chip.get_line(LINE_BTN)
btn.request(consumer="nutbam", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

# Lấy line cho LED
led = chip.get_line(LINE_LED)
led.request(consumer="nutbam_led", type=gpiod.LINE_REQ_DIR_OUT)

def watcher():
    while True:
        if btn.event_wait():  # block tới khi có event
            ev = btn.event_read()
            if ev.type == gpiod.LineEvent.RISING_EDGE:
                print("[EVENT] RISING")
                led.set_value(1)  # bật LED
            elif ev.type == gpiod.LineEvent.FALLING_EDGE:
                print("[EVENT] FALLING")
                led.set_value(0)  # tắt LED

t = threading.Thread(target=watcher, daemon=True)
t.start()

print("Chờ nút bấm... Ctrl+C để thoát")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    btn.release()
    led.release()
    chip.close()
