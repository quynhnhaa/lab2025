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

# Cấu hình nút là input với ngắt FALLING_EDGE (nhấn)
button.request(consumer="button", type=gpiod.LINE_REQ_EV_FALLING_EDGE)

# Biến trạng thái LED
led_state = 0
led.set_value(led_state)

print("Đang chờ nút nhấn để đổi trạng thái LED...")

try:
    while True:
        if button.event_wait(sec=10):  # Chờ tối đa 10 giây
            evt = button.event_read()
            if evt.type == gpiod.LineEvent.FALLING_EDGE:
                led_state = 1 - led_state  # Đảo trạng thái
                led.set_value(led_state)
                print(f"LED {'bật' if led_state else 'tắt'}")
        else:
            print("Không có sự kiện trong 10 giây")
except KeyboardInterrupt:
    print("Thoát chương trình")
