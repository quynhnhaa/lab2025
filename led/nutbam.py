import lgpio
import time

BUTTON_PIN = 17   # BCM pin cho nút
LED_PIN = 27      # BCM pin cho LED

# Mở chip GPIO (chip số 0)
chip = lgpio.gpiochip_open(0)

# Cấu hình chân
lgpio.gpio_claim_input(chip, BUTTON_PIN)
lgpio.gpio_claim_output(chip, LED_PIN)

# Hàm callback khi có ngắt
def button_callback(chip, gpio, level, tick, userdata):
    print(f"[CALLBACK] GPIO{gpio} Level={level} Tick={tick}")
    if level == 1:   # Nút nhấn xuống
        lgpio.gpio_write(chip, LED_PIN, 1)
    elif level == 0: # Nút nhả ra
        lgpio.gpio_write(chip, LED_PIN, 0)

# Chống dội 200ms
lgpio.gpio_set_debounce_micros(chip, BUTTON_PIN, 200000)

# Đăng ký ngắt cho cả 2 cạnh
lgpio.gpio_claim_alert(chip, BUTTON_PIN, lgpio.BOTH_EDGES)
lgpio.gpio_set_alert_func_ex(chip, BUTTON_PIN, button_callback, None)

print("Chờ nút bấm... (Ctrl+C để thoát)")
try:
    while True:
        time.sleep(1)  # callback chạy ngầm khi có ngắt
except KeyboardInterrupt:
    print("Thoát...")
    lgpio.gpiochip_close(chip)
