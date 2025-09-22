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

# Hàm callback khi có ngắt
def button_callback(chip, gpio, level, tick):
    print(f"[CALLBACK] Pin {gpio} Level {level} Tick {tick}")
    if level == 1:  # Nhấn nút
        lgpio.gpio_write(chip, LED_PIN, 1)
    elif level == 0:  # Nhả nút
        lgpio.gpio_write(chip, LED_PIN, 0)

# Chống dội 200ms
lgpio.gpio_set_debounce_micros(chip, BUTTON_PIN, 200000)

# Đăng ký callback cho rising + falling
lgpio.gpio_claim_alert(chip, BUTTON_PIN, lgpio.RISING_EDGE | lgpio.FALLING_EDGE)
lgpio.gpio_set_callbacks(chip, BUTTON_PIN, button_callback)

print("Chờ nút bấm... Ctrl+C để thoát")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Thoát...")
    lgpio.gpiochip_close(chip)
