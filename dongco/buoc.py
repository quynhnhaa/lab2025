# # import RPi.GPIO as GPIO
# # import time

# # in1 = 17
# # in2 = 18
# # in3 = 27
# # in4 = 22

# # # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
# # step_sleep = 0.002

# # step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

# # direction = False # True for clockwise, False for counter-clockwise

# # # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
# # step_sequence = [[1,0,0,1],
# #                  [1,0,0,0],
# #                  [1,1,0,0],
# #                  [0,1,0,0],
# #                  [0,1,1,0],
# #                  [0,0,1,0],
# #                  [0,0,1,1],
# #                  [0,0,0,1]]

# # # setting up
# # GPIO.setmode( GPIO.BCM )
# # GPIO.setup( in1, GPIO.OUT )
# # GPIO.setup( in2, GPIO.OUT )
# # GPIO.setup( in3, GPIO.OUT )
# # GPIO.setup( in4, GPIO.OUT )

# # # initializing
# # GPIO.output( in1, GPIO.LOW )
# # GPIO.output( in2, GPIO.LOW )
# # GPIO.output( in3, GPIO.LOW )
# # GPIO.output( in4, GPIO.LOW )

# # motor_pins = [in1,in2,in3,in4]
# # motor_step_counter = 0 ;

# # def cleanup():
# #     GPIO.output( in1, GPIO.LOW )
# #     GPIO.output( in2, GPIO.LOW )
# #     GPIO.output( in3, GPIO.LOW )
# #     GPIO.output( in4, GPIO.LOW )
# #     GPIO.cleanup()

# # # the meat
# # try:
# #     i = 0
# #     for i in range(step_count):
# #         for pin in range(0, len(motor_pins)):
# #             GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
# #         if direction==True:
# #             motor_step_counter = (motor_step_counter - 1) % 8
# #         elif direction==False:
# #             motor_step_counter = (motor_step_counter + 1) % 8
# #         else: # defensive programming
# #             print( "uh oh... direction should *always* be either True or False" )
# #             cleanup()
# #             exit( 1 )
# #         time.sleep( step_sleep )

# # except KeyboardInterrupt:
# #     cleanup()
# #     exit( 1 )

# # cleanup()
# # exit( 0 )

# import RPi.GPIO as GPIO
# import time

# # Thiết lập chế độ đánh số chân
# GPIO.setmode(GPIO.BCM)

# # Khai báo các chân điều khiển
# IN1 = 6
# IN2 = 13
# IN3 = 19
# IN4 = 26

# control_pins = [IN1, IN2, IN3, IN4]

# # Thiết lập các chân là output
# for pin in control_pins:
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, 0)

# # Chuỗi bước nửa bước (half-step) cho 28BYJ-48
# halfstep_seq = [
#     [1,0,0,0],
#     [1,1,0,0],
#     [0,1,0,0],
#     [0,1,1,0],
#     [0,0,1,0],
#     [0,0,1,1],
#     [0,0,0,1],
#     [1,0,0,1]
# ]

# def step_motor(steps, delay=0.001):
#     direction = 1 if steps > 0 else -1
#     steps = abs(steps)
#     for _ in range(steps):
#         for step in range(8)[::direction]:
#             for pin in range(4):
#                 GPIO.output(control_pins[pin], halfstep_seq[step][pin])
#             time.sleep(delay)

# try:
#     while True:
#         print("Quay thuận 520 bước (360 độ)")
#         step_motor(520)
#         time.sleep(1)

#         print("Quay ngược 260 bước (180 độ)")
#         step_motor(-260)
#         time.sleep(1)



# except KeyboardInterrupt:
#     print("Dừng bởi người dùng")
#     print("Dừng động cơ")
#     for pin in control_pins:
#         GPIO.output(pin, 0)

# finally:
#     GPIO.cleanup()


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

IN1, IN2, IN3, IN4 = 6, 13, 19, 26
control_pins = [IN1, IN2, IN3, IN4]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

halfstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

STEPS_PER_REV = 524  # số half-steps cho 360 độ

def step_motor(steps, delay=0.001):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    for _ in range(steps):
        for step in range(8)[::direction]:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[step][pin])
            time.sleep(delay)

def rotate_degree(degree, delay=0.001):
    steps = int(degree * STEPS_PER_REV / 360)
    step_motor(steps, delay)

try:
    while True:
        print("Quay thuận 360 độ")
        rotate_degree(360)   # quay 1 vòng
        time.sleep(1)

        print("Quay ngược 180 độ")
        rotate_degree(-180)  # quay nửa vòng ngược lại
        time.sleep(1)

except KeyboardInterrupt:
    print("Dừng bởi người dùng")
    for pin in control_pins:
        GPIO.output(pin, 0)

finally:
    GPIO.cleanup()
