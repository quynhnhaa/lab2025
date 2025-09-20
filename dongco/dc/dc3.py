# import RPi.GPIO as GPIO
# from time import sleep

# in1 = 27
# in2 = 22
# en = 17
# temp1=1

# GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(in1,GPIO.OUT)
# GPIO.setup(in2,GPIO.OUT)
# GPIO.setup(en,GPIO.OUT)
# GPIO.output(in1,GPIO.LOW)
# GPIO.output(in2,GPIO.LOW)

# p=GPIO.PWM(en,1000)
# p.start(25)
# print("\n")
# print("The default speed & direction of motor is LOW & Forward.....")
# print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
# print("\n")

# while(1):

#     x=input()

#     if x=='r':
#         print("run")
#         if(temp1==1):
#          GPIO.output(in1,GPIO.HIGH)
#          GPIO.output(in2,GPIO.LOW)
#          print("forward")
#          x='z'
#         else:
#          GPIO.output(in1,GPIO.LOW)
#          GPIO.output(in2,GPIO.HIGH)
#          print("backward")
#          x='z'


#     elif x=='s':
#         print("stop")
#         GPIO.output(in1,GPIO.LOW)
#         GPIO.output(in2,GPIO.LOW)
#         x='z'

#     elif x=='f':
#         print("forward")
#         GPIO.output(in1,GPIO.HIGH)
#         GPIO.output(in2,GPIO.LOW)
#         temp1=1
#         x='z'

#     elif x=='b':
#         print("backward")
#         GPIO.output(in1,GPIO.LOW)
#         GPIO.output(in2,GPIO.HIGH)
#         temp1=0
#         x='z'

#     elif x=='l':
#         print("low")
#         p.ChangeDutyCycle(25)
#         x='z'

#     elif x=='m':
#         print("medium")
#         p.ChangeDutyCycle(50)
#         x='z'

#     elif x=='h':
#         print("high")
#         p.ChangeDutyCycle(75)
#         x='z'


#     elif x=='e':
#         GPIO.cleanup()
#         break

#     else:
#         print("<<<  wrong data  >>>")
#         print("please enter the defined data to continue.....")


import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Khai báo chân
IN1 = 17
IN2 = 27
ENA = 22

# Thiết lập chân là output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Tạo PWM trên chân ENA với tần số 1000Hz
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)  # Bắt đầu với duty cycle = 0

def forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        print("Forward 50%")
        forward(50)
        time.sleep(5)

        print("Stop")
        stop()
        time.sleep(2)

        print("Backward 25%")
        backward(25)
        time.sleep(5)

        print("Stop")
        stop()

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    pwm.stop()
    GPIO.cleanup()
