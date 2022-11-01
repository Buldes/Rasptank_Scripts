# Import
import sys
import socket
import _thread
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
from rpi_ws281x import *
import sys_info

# Message
print("Server starts ...")


'Einstellen'

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

#Ultrasonic - Sensor
trigger = 11
ec = 8
GPIO.setup(trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ec, GPIO.IN)


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
color = Color(255,0,0)
for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
    strip.show()

# Line tracking Module
GPIO.setup(19, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(20, GPIO.IN)

'Variable'
# ---------------------------------------------------------------------
servo_11_position = 360
servo_12_position = 360
servo_13_position = 360
servo_14_position = 360
servo_15_position = 360
# ---------------------------------------------------------------------
move_arm_Variable = True
color_arm_stop = False
w_erlauben = True
Motor_A_EN = 4
Motor_A_Pin1 = 14
Motor_A_Pin2 = 15
Motor_B_EN = 17
Motor_B_Pin1 = 27
Motor_B_Pin2 = 18
color_wait_stop = False

'Definitionen'

# Servos
def cleanup():
    for a in range(12, 15):
        servo.set_pwm(a, 0, 360)
    servo.set_pwm(15, 0, 215)
    servo.set_pwm(11, 0, 200)

def move_arm(servo_nr, positon):
    servo.set_pwm(servo_nr, 0, positon)

def move_arm_plus(servo_nr):
    global move_arm_Variable
    global servo_11_position
    global servo_12_position
    global servo_13_position
    global servo_14_position
    global servo_15_position
    while move_arm_Variable:
        time.sleep(0.01)
        if servo_nr == 11 and servo_11_position <= 240:
            servo_11_position += 1
            move_arm(servo_nr, servo_11_position)
        elif servo_nr == 12 and servo_12_position <= 360:
            servo_12_position += 1
            move_arm(servo_nr, servo_12_position)
        elif servo_nr == 13 and servo_13_position <= 360:
            servo_13_position += 1
            move_arm(servo_nr, servo_13_position)
        elif servo_nr == 14 and servo_14_position <= 600:
            servo_14_position += 1
            move_arm(servo_nr, servo_14_position)
        elif servo_nr == 15 and servo_15_position <= 280:
            servo_15_position += 1
            move_arm(servo_nr, servo_15_position)

def move_arm_minus(servo_nr):
    global move_arm_Variable
    global servo_11_position
    global servo_12_position
    global servo_13_position
    global servo_14_position
    global servo_15_position
    while move_arm_Variable:
        time.sleep(0.01)
        if servo_nr == 11 and servo_11_position > 160:
            servo_11_position -= 1
            move_arm(servo_nr, servo_11_position)
        elif servo_nr == 12 and servo_12_position > 140:
            servo_12_position -= 1
            move_arm(servo_nr, servo_12_position)
        elif servo_nr == 13 and servo_13_position > 160:
            servo_13_position -= 1
            move_arm(servo_nr, servo_13_position)
        elif servo_nr == 14 and servo_14_position > 80:
            servo_14_position -= 1
            move_arm(servo_nr, servo_14_position)
        elif servo_nr == 15 and servo_15_position > 160:
            print(servo_15_position)
            servo_15_position -= 1
            move_arm(servo_nr, servo_15_position)

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

def move_motor(direction, speed = 70):
    if direction == "forward":
        motor_left("forward", speed)
        motor_right("forward", speed)
    elif direction == "backward":
        motor_left("backward", speed)
        motor_right("backward", speed)
    elif direction == "left":
        motor_right("forward", speed)
        motor_left("backward", speed)
    elif direction == "right":
        motor_right("backward", speed)
        motor_left("forward", speed)
    else:
        motor_right("stop", speed)
        motor_left("stop", speed)

def color_wipe(num, R, G, B):
    strip.setPixelColor(num, Color(R,G,B))
    strip.show()

def color_wait():
    global color_wait_stop
    while color_wait_stop == False:
        for b in range(0, 255):
            for a in range(0, 12):
                color_wipe(a, 0, 0, b)
            if color_wait_stop == True:
                break
            time.sleep(0.01)
        for b in reversed(range(0, 255)):
            for a in range(0, 12):
                color_wipe(a, 0, 0, b)
            if color_wait_stop == True:
                break
            time.sleep(0.01)

def color_move_left():
    global color_wait_stop
    for a in 7, 8, 10, 11:
        color_wipe(a, 20, 20, 20)
    for k in 6, 9:
        color_wipe(k, 20, 0, 0)
    while not color_wait_stop:
        for k in 2, 1, 4, 5:
            color_wipe(k, 5, 5, 5)
        for a in 0, 3:
            color_wipe(a, 5, 0, 0)
        time.sleep(0.75)
        if color_wait_stop:
            break
        for k in range(0, 6):
            color_wipe(k, 255, 50, 0)
        time.sleep(0.75)

def color_move_right():
    global color_wait_stop
    for e in 2, 1, 4, 5:
        color_wipe(e, 20, 20, 20)
    for u in 0, 3:
        color_wipe(u, 20, 0, 0)
    while not color_wait_stop:
        for y in 7, 8, 10, 11:
            color_wipe(y, 5, 5, 5)
        for x in 6, 9:
            color_wipe(x, 5, 0, 0)
        time.sleep(0.75)
        if color_wait_stop:
            break
        for q in range(6, 12):
            color_wipe(q, 255, 50, 0)
        time.sleep(0.75)

def color_move_forward():
    for f in 2, 4, 5, 7, 8, 11, 10, 1:
        color_wipe(f, 255, 255, 255)
    for n in 0, 3, 6, 9:
        color_wipe(n, 10, 0, 0)

def color_move_backward():
    for p in 2, 4, 5, 7, 8, 11, 10, 1:
        color_wipe(p, 10, 10, 10)
    for o in 0, 3, 6, 9:
        color_wipe(o, 255, 0, 0)

def color_arm():
    for v in 0, 4, 2, 6, 10, 8:
        color_wipe(v, 255, 215, 0)

    for b in 3, 1, 5, 9, 7, 11:
        color_wipe(b, 255, 0, 0)

def line_tracking_modul():
    status_right = GPIO.input(19)
    status_left = GPIO.input(20)
    status_middle = GPIO.input(16)

    return status_left, status_middle, status_right

def USS_messen():
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(trigger, GPIO.LOW)
    while not GPIO.input(ec):
        pass
    t1 = time.time()
    while GPIO.input(ec):
        pass
    t2 = time.time()

    #Auswerten
    Abstand = round((t2-t1)*34300/2, 2)
    print(Abstand, "cm")

    return Abstand


def USS_Controll_and_diagnosis_send():
    global client
    global servo_11_position
    global servo_12_position
    global servo_13_position
    global servo_14_position
    global servo_15_position
    global w_erlauben
    while True:
        USS_Abstand = USS_messen()
        line = line_tracking_modul()
        time.sleep(0.1)

        client_send_tuple_1 = str("a" + str(servo_11_position) + str(servo_12_position) + str(servo_13_position)
                                + str(servo_14_position) + str(servo_15_position) + str(round(USS_Abstand, 2))
                                + str(line[0]) + str(line[1]) + str(line[2]))
        client_send_tuple_2 = "b" + str(sys_info.cpu_statistic()[0])
        client_send_tuple_3 = "c" + str(sys_info.cpu_statistic()[1])
        print(client_send_tuple_1)
        client.send(bytes(client_send_tuple_1, "utf8"))
        time.sleep(0.1)
        client.send(bytes(client_send_tuple_2, "utf8"))
        time.sleep(0.1)
        client.send(bytes(client_send_tuple_3, "utf8"))

        if USS_Abstand < 9.00:
            if w_erlauben:
                move_motor("stop")
            w_erlauben = False
            for K in range(0, 12):
                color_wipe(K, 255, 0, 0)
        else:
            w_erlauben = True


# color_wait() start
_thread.start_new_thread(color_wait, ())

'server'
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
server.bind((str(socket.gethostbyname(socket.gethostname())), 1501))
server.listen(1)

# Message
print("Server online.")
print("Your IP-Addres:", socket.gethostbyname(socket.gethostname()))

# Verbunden?
(client, addr) = server.accept()
time.sleep(0.5)
print("Connected")

# vorkehrungen
thread = _thread.start_new_thread(cleanup, ())
color_wait_stop = True
time.sleep(0.02)
for k in range(0, 12):
    color_wipe(k, 0, 125, 0)
_thread.start_new_thread(USS_Controll_and_diagnosis_send, ())

while 1:

    try:
        msg = str(client.recv(16384), "utf8")
    except KeyboardInterrupt:
        cleanup()
        sys.exit()

    color_wait_stop = False

    # Ermittlung
    if msg == "Motor:stop":
        move_motor("stop")
        move_arm_Variable = False
        color_wait_stop = True
        if color_arm_stop:
            for k in 1, 2, 4, 5, 7, 8, 10, 11:
                color_wipe(k, 100, 100, 100)
            for k in 0, 3, 9, 6:
                color_wipe(k, 100, 0, 0)
        print("Motor : Stop")
    elif msg == "w-go" and w_erlauben == True:
        color_arm_stop = True
        color_move_forward()
        move_motor("forward")
        print("Motor : forward")
    elif msg == "s-go":
        color_arm_stop = True
        color_move_backward()
        move_motor("backward")
        print("Motor : backward)
    elif msg == "a-go":
        color_arm_stop = True
        _thread.start_new_thread(color_move_left, ())
        move_motor("left")
        print("Motor : left)
    elif msg == "d-go":
        color_arm_stop = True
        _thread.start_new_thread(color_move_right, ())
        move_motor("right")
        print("Motor : right)
    elif msg == "c-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_minus, (12, ))
        print("Arm-1. Motor : down)
    elif msg == "f-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_plus, (12, ))
        print("Arm-1. Motor : up")
    elif msg == "g-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_plus, (13, ))
        print("Arm-2.Motor : down")
    elif msg == "z-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_minus, (13, ))
        print("Arm-2.Motor : up")
    elif msg == "u-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_minus, (14, ))
        print("Arm-3.Motor : left")
    elif msg == "i-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_plus, (14, ))
        print("Arm-3.Motor : right")
    elif msg == "o-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_minus, (15, ))
        print("Arm-4.Motor : open")
    elif msg == "p-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_plus, (15, ))
        print("Arm-4.Motor : close")
    elif msg == "m-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_plus, (11, ))
        print("Kamera-Motor : down")
    elif msg == "k-go":
        color_arm_stop = False
        _thread.start_new_thread(color_arm, ())
        move_arm_Variable = True
        thread = _thread.start_new_thread(move_arm_minus, (11, ))
        print("Kamera-Motor : up")
    elif msg == "-VERBUNDEN-    -Test:2/3:OK" or msg == "-VERBUNDEN-    -Test:3/3:OK":
        print(msg)
    elif w_erlauben == True:
        pass
    else:
        print("--Unbekannte Date Entfangen--")
        print("    ", msg)
