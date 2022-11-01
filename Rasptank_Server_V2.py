"""Rasptank_Server_v2
    - No Cam
    - Connectable: Rasptank_Server_V2.2"""

"Imports"
import sys
import socket
import _thread
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
from rpi_ws281x import *
import sys_info

print("Server started...")

"[Einstellen]"

# Adafruit_PCA9685
servo = Adafruit_PCA9685.PCA9685()
servo.set_pwm_freq(50)

# Servo
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for a in 4, 14, 15, 17, 27, 18:
    exec("GPIO.setup(" + str(a) + ", GPIO.OUT)")
pwm_A = GPIO.PWM(4, 1000)
pwm_B = GPIO.PWM(17, 1000)

# Ultraschallsensor
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)  # trigger
GPIO.setup(8, GPIO.IN)  # ec

# rpi_ws281x
LED_COUNT = 12
LED_PIN = 12
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
strip = Adafruit_NeoPixel(LED_COUNT,
                          LED_PIN,
                          LED_FREQ_HZ,
                          LED_DMA,
                          LED_INVERT,
                          LED_BRIGHTNESS,
                          LED_CHANNEL)
strip.begin()
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()

# Line tracking Module
GPIO.setup(19, GPIO.IN)  # 1. Sensor
GPIO.setup(16, GPIO.IN)  # 2. Sensor
GPIO.setup(20, GPIO.IN)  # 3. Sensor

# Variables
servo_11_position = 360
servo_12_position = 360
servo_13_position = 360
servo_14_position = 360
servo_15_position = 360
move_arm_Variable = True
color_arm_stop = False
w_erlauben = True
Motor_A_EN = 4
Motor_A_Pin1 = 14
Motor_A_Pin2 = 15
Motor_B_EN = 17
Motor_B_Pin1 = 27
Motor_B_Pin2 = 18
color_breath_stop = False
color_ani = "none"
pressed_key = [False, False, False, False]  # w, a, s, d
pressed_arm = dict(c=False, f=False, g=False, z=False, u=False, i=False, o=False, p=False, m=False, k=False)

"Definitions"


def cleanup():
    for num_ in range(12, 15):
        servo.set_pwm(num_, 0, 360)
    servo.set_pwm(15, 0, 215)
    servo.set_pwm(11, 0, 200)
    for num_ in range(strip.numPixels()):
        strip.setPixelColor(num_, Color(255, 0, 0))
        strip.show()


def move_arm(servo_nr, pos):
    servo.set_pwm(servo_nr, 0, pos)


def move_arm_plus(servo_nr):
    global servo_11_position, servo_12_position, servo_13_position, servo_14_position, servo_15_position

    if servo_nr == 11 and servo_11_position <= 240:
        servo_11_position += 1
        move_arm(servo_nr, servo_11_position)
    if servo_nr == 12 and servo_12_position <= 360:
        servo_12_position += 1
        move_arm(servo_nr, servo_12_position)
    if servo_nr == 13 and servo_13_position <= 360:
        servo_13_position += 1
        move_arm(servo_nr, servo_13_position)
    if servo_nr == 14 and servo_14_position <= 600:
        servo_14_position += 1
        move_arm(servo_nr, servo_14_position)
    if servo_nr == 15 and servo_15_position <= 280:
        servo_15_position += 1
        move_arm(servo_nr, servo_15_position)


def move_arm_minus(servo_nr):
    global servo_11_position, servo_12_position, servo_13_position, servo_14_position, servo_15_position

    if servo_nr == 11 and servo_11_position > 160:
        servo_11_position -= 1
        move_arm(servo_nr, servo_11_position)
    if servo_nr == 12 and servo_12_position > 140:
        servo_12_position -= 1
        move_arm(servo_nr, servo_12_position)
    if servo_nr == 13 and servo_13_position > 160:
        servo_13_position -= 1
        move_arm(servo_nr, servo_13_position)
    if servo_nr == 14 and servo_14_position > 80:
        servo_14_position -= 1
        move_arm(servo_nr, servo_14_position)
    if servo_nr == 15 and servo_15_position > 160:
        servo_15_position -= 1
        move_arm(servo_nr, servo_15_position)


def main_control():
    global pressed_arm, color_ani, pressed_key

    while True:
        time.sleep(0.005)

        # Arm
        if pressed_arm["k"]:
            move_arm_plus(11)
            color_ani = "arm"
        if pressed_arm["f"]:
            move_arm_plus(12)
            color_ani = "arm"
        if pressed_arm["z"]:
            move_arm_minus(13)
            color_ani = "arm"
        if pressed_arm["i"]:
            move_arm_plus(14)
            color_ani = "arm"
        if pressed_arm["p"]:
            move_arm_plus(15)
            color_ani = "arm"

        if pressed_arm["m"]:
            move_arm_minus(11)
            color_ani = "arm"
        if pressed_arm["c"]:
            move_arm_minus(12)
            color_ani = "arm"
        if pressed_arm["g"]:
            move_arm_plus(13)
            color_ani = "arm"
        if pressed_arm["u"]:
            move_arm_minus(14)
            color_ani = "arm"
        if pressed_arm["o"]:
            move_arm_minus(15)
            color_ani = "arm"

        # Move
        if not w_erlauben:
            pressed_key[0] = False

        if pressed_key[0] and pressed_key[1] and pressed_key[2] == False and pressed_key[3] == False:  # w+a
            motor_right("forward", speed=80)
            motor_left("forward", speed=5)
            color_ani = "left"
        elif pressed_key[0] and pressed_key[3] and pressed_key[2] == False and pressed_key[1] == False:  # w+d
            motor_right("forward", speed=5)
            motor_left("forward", speed=80)
            color_ani = "right"
        elif pressed_key[2] and pressed_key[1] and pressed_key[0] == False and pressed_key[3] == False:  # s+a
            motor_right("backward", speed=80)
            motor_left("backward", speed=5)
            color_ani = "backward"
        elif pressed_key[2] and pressed_key[3] and pressed_key[0] == False and pressed_key[1] == False:  # s+d
            motor_right("backward", speed=5)
            motor_left("backward", speed=80)
            color_ani = "backward"
        elif pressed_key[0] and pressed_key[1] == False and pressed_key[2] == False and pressed_key[3] == False:  # w
            motor_right("forward", speed=70)
            motor_left("forward", speed=70)
            color_ani = "forward"
        elif pressed_key[0] == False and pressed_key[1] and pressed_key[2] == False and pressed_key[3] == False:  # a
            motor_right("forward", speed=70)
            motor_left("backward", speed=70)
            color_ani = "left"
        elif pressed_key[0] == False and pressed_key[1] == False and pressed_key[2] and pressed_key[3] == False:  # s
            motor_right("backward", speed=60)
            motor_left("backward", speed=60)
            color_ani = "backward"
        elif pressed_key[0] == False and pressed_key[1] == False and pressed_key[2] == False and pressed_key[3]:  # d
            motor_right("backward", speed=70)
            motor_left("forward", speed=70)
            color_ani = "right"
        else:
            motor_right("stop", speed=0)
            motor_left("stop", speed=0)
            color_ani = "forward"


def motor_right(direction, speed):
    if direction != "forward" and direction != "backward":
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        pwm_B.start(100)
        pwm_B.ChangeDutyCycle(speed)
    elif direction == "forward":
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)
        pwm_B.start(0)
        pwm_B.ChangeDutyCycle(speed)


def motor_left(direction, speed):
    if direction != "forward" and direction != "backward":
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
    elif direction == "forward":
        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        pwm_A.start(100)
        pwm_A.ChangeDutyCycle(speed)
    elif direction == "backward":
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        pwm_A.start(0)
        pwm_A.ChangeDutyCycle(speed)


def color_wipe(pos, R, G, B):
    strip.setPixelColor(pos, Color(R, G, B))
    strip.show()


def color_breath_ani():
    global color_breath_stop

    while not color_breath_stop:
        for b in range(0, 255):
            for number in range(0, 12):
                color_wipe(number, 0, 0, b)
            if color_breath_stop:
                break
            time.sleep(0.01)
        for b in reversed(range(0, 255)):
            for number in range(0, 12):
                color_wipe(number, 0, 0, b)
            if color_breath_stop:
                break
            time.sleep(0.01)


def color_animation():
    global color_ani

    while True:
        if color_ani == "left":
            for nr in 7, 8, 10, 11:
                color_wipe(nr, 20, 20, 20)
            for k in 6, 9:
                color_wipe(k, 20, 0, 0)

            while color_ani == "left":
                for k in 2, 1, 4, 5:
                    color_wipe(k, 5, 5, 5)
                for nr in 0, 3:
                    color_wipe(nr, 5, 0, 0)

                for wait in range(0, 3):
                    time.sleep(0.25)
                    if color_ani != "left":
                        break

                for nr in range(0, 6):
                    color_wipe(nr, 255, 50, 0)
                time.sleep(0.75)

        elif color_ani == "right":
            for nr in 2, 1, 4, 5:
                color_wipe(nr, 20, 20, 20)
            for nr in 0, 3:
                color_wipe(nr, 20, 0, 0)

            while color_ani == "right":
                for nr in 7, 8, 10, 11:
                    color_wipe(nr, 5, 5, 5)
                for nr in 6, 9:
                    color_wipe(nr, 5, 0, 0)
                time.sleep(0.75)

                for wait in range(0, 3):
                    time.sleep(0.25)
                    if color_ani != "right":
                        break

                for nr in range(6, 12):
                    color_wipe(nr, 255, 50, 0)

                for wait in range(0, 3):
                    time.sleep(0.25)
                    if color_ani != "right":
                        break

        elif color_ani == "forward":
            for nr in 2, 4, 5, 7, 8, 11, 10, 1:
                color_wipe(nr, 255, 255, 255)
            for nr in 0, 3, 6, 9:
                color_wipe(nr, 10, 0, 0)

        elif color_ani == "backward":
            for nr in 2, 4, 5, 7, 8, 11, 10, 1:
                color_wipe(nr, 10, 10, 10)
            for nr in 0, 3, 6, 9:
                color_wipe(nr, 255, 0, 0)

        elif color_ani == "arm":
            for nr in 0, 4, 2, 6, 10, 8:
                color_wipe(nr, 255, 215, 0)

            for nr in 3, 1, 5, 9, 7, 11:
                color_wipe(nr, 255, 0, 0)


def send_data():
    global servo_11_position, servo_12_position, servo_13_position, servo_14_position, servo_15_position
    global w_erlauben, client
    while True:

        GPIO.output(11, GPIO.HIGH)  # trigger
        time.sleep(0.000015)
        GPIO.output(11, GPIO.LOW)  # trigger
        while not GPIO.input(8):
            pass
        t1 = time.time()
        while GPIO.input(8):
            pass
        t2 = time.time()

        USS_Abstand = round((t2 - t1) * 34300 / 2, 2)

        line = [GPIO.input(20), GPIO.input(16), GPIO.input(19)]

        time.sleep(0.2)

        client_send_tuple_1 = str("a" + str(int(servo_11_position)) + str(servo_12_position) + str(servo_13_position)
                                  + str(servo_14_position) + str(servo_15_position) + str(round(USS_Abstand, 2))
                                  + str(line[0]) + str(line[1]) + str(line[2]))
        client_send_tuple_2 = "b" + str(sys_info.cpu_statistic()[0])
        client_send_tuple_3 = "c" + str(sys_info.cpu_statistic()[1])
        client.send(bytes(client_send_tuple_1, "utf8"))
        time.sleep(0.3)
        client.send(bytes(client_send_tuple_2, "utf8"))
        time.sleep(0.2)
        client.send(bytes(client_send_tuple_3, "utf8"))

        if USS_Abstand < 9.00:
            if w_erlauben:
                motor_right("stop", speed=70)
                motor_left("stop", speed=70)
            w_erlauben = False
            for K in range(0, 12):
                color_wipe(K, 255, 0, 0)
        else:
            w_erlauben = True


# Wait Animation
_thread.start_new_thread(color_breath_ani, ())

"Server"
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

server.bind((str(socket.gethostbyname(socket.gethostname())), 1501))
server.listen(1)

print("Server online... \nWaiting for Connection.")
print("Your IP-Addres: ", socket.gethostbyname(socket.gethostname()))

# Connected
try:
    (client, addr) = server.accept()
    time.sleep(0.5)
    color_breath_stop = True
except:
    print("[Error] Connection failed. \n Programm canceled...")
    sys.exit()

print("Verbunden")

"Start Programm"
cleanup()
for num in range(0, 12):
    color_wipe(num, 0, 125, 0)
color_th = _thread.start_new_thread(color_animation, ())
control_th = _thread.start_new_thread(main_control, ())
_thread.start_new_thread(send_data, ())

"receive data"
while True:

    try:
        msg = str(client.recv(128), "UTF8")
    except:
        print("Conection lost \n Program canceled...")
        cleanup()
        sys.exit()

    # analyze

    if msg == "w-press":
        pressed_key[0] = True
    if msg == "a-press":
        pressed_key[1] = True
    if msg == "s-press":
        pressed_key[2] = True
    if msg == "d-press":
        pressed_key[3] = True

    if msg == "w-release":
        pressed_key[0] = False
    if msg == "a-release":
        pressed_key[1] = False
    if msg == "s-release":
        pressed_key[2] = False
    if msg == "d-release":
        pressed_key[3] = False

    if msg == "f-press":
        pressed_arm["f"] = True
    if msg == "z-press":
        pressed_arm["z"] = True
    if msg == "i-press":
        pressed_arm["i"] = True
    if msg == "p-press":
        pressed_arm["p"] = True
    if msg == "k-press":
        pressed_arm["k"] = True

    if msg == "c-press":
        pressed_arm["c"] = True
    if msg == "g-press":
        pressed_arm["g"] = True
    if msg == "u-press":
        pressed_arm["u"] = True
    if msg == "o-press":
        pressed_arm["o"] = True
    if msg == "m-press":
        pressed_arm["m"] = True

    if msg == "f-release":
        pressed_arm["f"] = False
    if msg == "z-release":
        pressed_arm["z"] = False
    if msg == "i-release":
        pressed_arm["i"] = False
    if msg == "p-release":
        pressed_arm["p"] = False
    if msg == "k-release":
        pressed_arm["k"] = False

    if msg == "c-release":
        pressed_arm["c"] = False
    if msg == "g-release":
        pressed_arm["g"] = False
    if msg == "u-release":
        pressed_arm["u"] = False
    if msg == "o-release":
        pressed_arm["o"] = False
    if msg == "m-release":
        pressed_arm["m"] = False
