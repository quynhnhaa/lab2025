# import RPi.GPIO as GPIO
# import time
 
# #GPIO Mode (BOARD / BCM)
# GPIO.setmode(GPIO.BCM)
 
# #set GPIO Pins
# GPIO_TRIGGER = 18
# GPIO_ECHO = 24
 
# #set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
# GPIO.setup(GPIO_ECHO, GPIO.IN)
 
# def distance():
#     # set Trigger to HIGH
#     GPIO.output(GPIO_TRIGGER, True)
 
#     # set Trigger after 0.01ms to LOW
#     time.sleep(0.00001)
#     GPIO.output(GPIO_TRIGGER, False)
 
#     StartTime = time.time()
#     StopTime = time.time()
 
#     # save StartTime
#     while GPIO.input(GPIO_ECHO) == 0:
#         StartTime = time.time()
 
#     # save time of arrival
#     while GPIO.input(GPIO_ECHO) == 1:
#         StopTime = time.time()
 
#     # time difference between start and arrival
#     TimeElapsed = StopTime - StartTime
#     # multiply with the sonic speed (34300 cm/s)
#     # and divide by 2, because there and back
#     distance = (TimeElapsed * 34300) / 2
 
#     return distance
 
# if __name__ == '__main__':
#     try:
#         while True:
#             dist = distance()
#             print ("Measured Distance = %.1f cm" % dist)
#             time.sleep(1)
 
#         # Reset by pressing CTRL + C
#     except KeyboardInterrupt:
#         print("Measurement stopped by User")
#         GPIO.cleanup()

import time
import RPi.GPIO as GPIO

# Khai báo sử dụng cách đánh dấu PIN theo BCM
# Có 2 kiểu đánh dấu PIN là BCM và BOARD
GPIO.setmode(GPIO.BCM)

# Khởi tạo 2 biến chứa GPIO ta sử dụng
GPIO_TRIGGER = 23
GPIO_ECHO = 24

print("Ultrasonic Measurement")

# Thiết lập GPIO nào để gửi tiến hiệu và nhận tín hiệu
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Khai báo này ám chỉ việc hiện tại không gửi tín hiệu điện
# qua GPIO này, kiểu kiểu ngắt điện ấy
GPIO.output(GPIO_TRIGGER, False)

# Cái này mình cũng không rõ, nhưng họ bảo là để khởi động cảm biến
time.sleep(0.5)

# Kích hoạt cảm biến bằng cách ta nháy cho nó tí điện rồi ngắt đi luôn.
GPIO.output(GPIO_TRIGGER, True)
time.sleep(0.00001)
GPIO.output(GPIO_TRIGGER, False)

# Đánh dấu thời điểm bắt đầu
start = time.time()
while GPIO.input(GPIO_ECHO)==0:
  start = time.time()
# Bắt thời điểm nhận được tín hiệu từ Echo
while GPIO.input(GPIO_ECHO)==1:
  stop = time.time()

# Thời gian từ lúc gửi tín hiêu
elapsed = stop-start

# Distance pulse travelled in that time is time
# multiplied by the speed of sound (cm/s)
distance = elapsed * 34000

# That was the distance there and back so halve the value
distance = distance / 2

print("Distance : %.1f" % distance)

# Reset GPIO settings
GPIO.cleanup()