import gpiod
import time

CHIP = "gpiochip0"
BUTTON_LINE = 16
LED_LINE = 20

# Mở chip GPIO
chip = gpiod.Chip(CHIP)

# Lấy line cho nút và LED
button = chip.get_line(BUTTON_LINE)
led = chip.get_line(LED_LINE)

# Cấu hình LED là output
led.request(consumer="led", type=gpiod.LINE_REQ_DIR_OUT)

# Cấu hình nút là input với ngắt cả RISING và FALLING
button.request(consumer="button", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

print("Đang chờ sự kiện nút...")

try:
    while True:
        event = button.event_wait(sec=5)  # Chờ tối đa 5 giây
        if event:
            evt = button.event_read()
            if evt.type == gpiod.LineEvent.FALLING_EDGE:
                print("Nút được nhấn")
                led.set_value(1)
            elif evt.type == gpiod.LineEvent.RISING_EDGE:
                print("Nút được thả")
                led.set_value(0)
        else:
            print("Không có sự kiện trong 5 giây")
except KeyboardInterrupt:
    print("Thoát chương trình")
