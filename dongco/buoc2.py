import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# coil_A_1_pin = 13 # 4 pink. IN_B
# coil_A_2_pin = 26 # 17 orange IN_D
# coil_B_1_pin = 6  # 23 blue. IN_A
# coil_B_2_pin = 19 # 24 yellow. IN_C

IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26


# adjust if different
StepCount=8
Seq = [
    [0,1,0,0],
    [0,1,0,1],
    [0,0,0,1],
    [1,0,0,1],
    [1,0,0,0],
    [1,0,1,0],
    [0,0,1,0],
    [0,1,1,0]
    ]


GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


def setStep(w1, w2, w3, w4):
    GPIO.output(IN2, w1)
    GPIO.output(IN4, w2)
    GPIO.output(IN1, w3)
    GPIO.output(IN3, w4)

def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

if __name__ == '__main__':
    while True:
        delay = input("Time Delay (ms)?")
        steps = input("How many steps forward? ")
        forward(int(delay) / 1000.0, int(steps))
        steps = input("How many steps backwards? ")
        backwards(int(delay) / 1000.0, int(steps))
