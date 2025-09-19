import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

coil_A_1_pin = 13 # 4 pink. IN_B
coil_A_2_pin = 26 # 17 orange IN_D
coil_B_1_pin = 6  # 23 blue. IN_A
coil_B_2_pin = 19 # 24 yellow. IN_C

IN_A = 6
IN_B = 13
IN_C = 19
IN_D = 26


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


GPIO.setup(IN_A, GPIO.OUT)
GPIO.setup(IN_B, GPIO.OUT)
GPIO.setup(IN_C, GPIO.OUT)
GPIO.setup(IN_D, GPIO.OUT)


def setStep(w1, w2, w3, w4):
    GPIO.output(IN_B, w1)
    GPIO.output(IN_D, w2)
    GPIO.output(IN_A, w3)
    GPIO.output(IN_C, w4)

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
