import gpiod
import threading
import time

CHIP = "gpiochip0"   # thường là /dev/gpiochip0
LINE = 17            # BCM offset — nếu dùng offset khác, hãy dùng gpioinfo để kiểm tra

chip = gpiod.Chip(CHIP)
line = chip.get_line(LINE)
# request for both edges
line.request(consumer="nutbam", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

def watcher():
    while True:
        # block until event (None / sec=None -> block indefinitely)
        if line.event_wait(sec=None):
            ev = line.event_read()
            if ev.type == gpiod.LineEvent.RISING_EDGE:
                print("[EVENT] RISING")
                # gọi callback / thao tác với LED ở đây
            else:
                print("[EVENT] FALLING")

t = threading.Thread(target=watcher, daemon=True)
t.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    line.release()
    chip.close()
