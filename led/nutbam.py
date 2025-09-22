import lgpio
import time

# Pin BCM
BUTTON_PIN = 17
LED_PIN = 27

# Mở chip GPIO
chip = lgpio.gpiochip_open(0)

# Cấu hình pin
lgpio.gpio_claim_input(chip, BUTTON_PIN)
lgpio.gpio_claim_output(chip, LED_PIN)

# Callback khi có ngắt
def button_callback(chip, gpio, level, tick):
    print(f"Nút thay đổi: {level}")
    if level == 1:  # Nhấn
        lgpio.gpio_write(chip, LED_PIN, 1)
    else:           # Nhả
        lgpio.gpio_write(chip, LED_PIN, 0)

# Đăng ký edge detection
lgpio.gpio_set_debounce_micros(chip, BUTTON_PIN, 200000)  # chống dội 200ms
lgpio.gpio_claim_alert(chip, BUTTON_PIN, lgpio.RISING_EDGE | lgpio.FALLING_EDGE)
lgpio.gpio_set_alert_func(chip, BUTTON_PIN, button_callback)

print("Chờ nút bấm... Ctrl+C để thoát")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Thoát...")
    lgpio.gpiochip_close(chip)
