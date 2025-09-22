import lgpio
import time

BUTTON_GPIO = 16
LED_GPIO = 20

h = lgpio.gpiochip_open(0)  # Mở chip GPIO mặc định

lgpio.gpio_claim_input(h, BUTTON_GPIO)
lgpio.gpio_claim_output(h, LED_GPIO)

def button_callback(chip, gpio, level, tick):
    if level == 0:  # Nút nhấn → LOW
        lgpio.gpio_write(h, LED_GPIO, 1)
    else:           # Nút thả → HIGH
        lgpio.gpio_write(h, LED_GPIO, 0)

# Đăng ký ngắt cho cả RISING và FALLING
lgpio.gpio_set_alert_func(h, BUTTON_GPIO, button_callback)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    lgpio.gpiochip_close(h)
