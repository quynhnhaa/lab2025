from gpiozero import Button
from signal import pause

button = Button(16, pull_up=True)

def on_press():
    print("Nút đã được nhấn!")

button.when_pressed = on_press

pause()
