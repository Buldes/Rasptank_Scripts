"""Rasptank Client V2 without cam"""
'Imports'
import tkinter as tk
import tkinter.messagebox as tk_message
import socket
import time
import _thread

'socket'
root = tk.Tk()
while 1:
    try:
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)

        ip_addr = '[youre ip address]

        server_addr = (ip_addr, 1501)

        client.connect(server_addr)
        time.sleep(0.2)
        client.send(bytes("-VERBUNDEN-    -Test:2/3:OK", "utf8"))
        client.send(bytes("-VERBUNDEN-    -Test:3/3:OK", "utf8"))
        break
    except:
        yesno = tk_message.askyesno("⛔Verbindung fehlgeschlagen", "Es konnte keine Verbindung zum Server hergestellt."
                                                                 "werden \n Soll versucht werden eine neue verbindung "
                                                                 "zu erstellen?")
        if yesno:
            continue
        break
root.destroy()

'Variable'
enter1 = True
enter2 = True
status = "main"
speed = 60
status_press = "none"
line_tracking_module = "none"

arm_11_position = 360
arm_12_position = 360
arm_13_position = 360
arm_14_position = 360
arm_15_position = 360

'Definition'
def w_press(event):
    global speed, status
    debug.configure(
        text="Chain: forward      (speed = " + str(speed) + ")")
    if status != "w":
        status = "w"
        client.send(bytes("w-go", "utf8"))


def a_press(event):
    global speed, status
    debug.configure(
        text="Chain: left         (speed = " + str(speed) + ")")
    if status != "a":
        status = "a"
        client.send(bytes("a-go", "utf8"))


def s_press(event):
    global speed, status
    debug.configure(
        text="chain: backward     (speed = " + str(speed) + ")")
    if status != "s":
        status = "s"
        client.send(bytes("s-go", "utf8"))


def d_press(event):
    global speed, status
    debug.configure(
        text="chain: right        (speed = " + str(speed) + ")")
    if status != "d":
        status = "d"
        client.send(bytes("d-go", "utf8"))


def arm_11_press_up(event):
    global arm_11_position, status
    debug.configure(text="Arm_11 =                  (degree = " + str(arm_11_position) + ")")
    if status != "arm_11_up":
        status = "arm_11_up"
        client.send(bytes("k-go", "utf8"))


def arm_12_press_up(event):
    global arm_12_position, status
    debug.configure(text="Arm_12 =                  (degree = " + str(arm_12_position) + ")")
    if status != "arm_12_up":
        status = "arm_12_up"
        client.send(bytes("f-go", "utf8"))


def arm_13_press_up(event):
    global arm_13_position, status
    debug.configure(text="Arm_13 =                  (degree = " + str(arm_13_position) + ")")
    if status != "arm_13_up":
        status = "arm_13_up"
        client.send(bytes("z-go", "utf8"))


def arm_14_press_left(event):
    global arm_14_position, status
    debug.configure(text="Arm_14 =                  (degree = " + str(arm_14_position) + ")")
    if status != "arm_14_left":
        status = "arm_14_left"
        client.send(bytes("u-go", "utf8"))


def arm_15_press_open(event):
    global arm_15_position, status
    debug.configure(text="Arm_15 =                  (degree = " + str(arm_15_position) + ")")
    if status != "arm_15_open":
        status = "arm_15_open"
        client.send(bytes("o-go", "utf8"))


def arm_11_press_down(event):
    global arm_11_position, status
    debug.configure(text="Arm_11 =                  (degree = " + str(arm_11_position) + ")")
    if status != "arm_11_down":
        status = "arm_11_down"
        client.send(bytes("m-go", "utf8"))


def arm_12_press_down(event):
    global arm_12_position, status
    debug.configure(text="Arm_12 =                  (degree = " + str(arm_12_position) + ")")
    if status != "arm_12_down":
        status = "arm_12_down"
        client.send(bytes("c-go", "utf8"))


def arm_13_press_down(event):
    global arm_13_position, status
    debug.configure(text="Arm_13 =                  (degree = " + str(arm_13_position) + ")")
    if status != "arm_13_down":
        status = "arm_13_down"
        client.send(bytes("g-go", "utf8"))


def arm_14_press_right(event):
    global arm_14_position, status
    debug.configure(text="Arm_14 =                  (degree = " + str(arm_14_position) + ")")
    if status != "arm_14_right":
        status = "arm_14_right"
        client.send(bytes("i-go", "utf8"))


def arm_15_press_close(event):
    global arm_15_position, status
    debug.configure(text="Arm_15 =                  (degree = " + str(arm_15_position) + ")")
    if status != "arm_15_close":
        status = "arm_15_close"
        client.send(bytes("p-go", "utf8"))


def stop_every(event):
    global status
    debug.configure(text="Every Motor stopped.")
    if status != "none":
        status = "none"
        client.send(bytes("Motor:stop", "utf8"))


def key_press(event):
    key = str(event)

    if "'w'" in key:
        w_press(1)
    elif "'d'" in key:
        d_press(1)
    elif "'s'" in key:
        s_press(1)
    elif "'a'" in key:
        a_press(1)
    elif "'c'" in key:
        arm_12_press_down(1)
    elif "'f'" in key:
        arm_12_press_up(1)
    elif "'g'" in key:
        arm_13_press_down(1)
    elif "'z'" in key:
        arm_13_press_up(1)
    elif "'i'" in key:
        arm_14_press_right(1)
    elif "'u'" in key:
        arm_14_press_left(1)
    elif "'o'" in key:
        arm_15_press_open(1)
    elif "'p'" in key:
        arm_15_press_close(1)
    elif "'k'" in key:
        arm_11_press_up(1)
    elif "'m'" in key:
        arm_11_press_down(1)


def uss_servo_cpu():
    global arm_11_position, arm_13_position, arm_14_position, arm_15_position, arm_12_position, line_tracking_module
    U_S_S_Scale_Variable = 100
    while 1:
        # server data
        input_server = str(client.recv(1684), "utf8")
        # len
        count = len(input_server)

        # evaluate
        # a
        if "a" in input_server:
            try:
                arm_11_position = int(input_server[0+1] + input_server[1+1] + input_server[2+1])
                arm_12_position = int(input_server[3+1] + input_server[4+1] + input_server[5+1])
                arm_13_position = int(input_server[6+1] + input_server[7+1] + input_server[6+1])
                arm_14_position = int(input_server[9+1] + input_server[10+1] + input_server[9+1])
                arm_15_position = int(input_server[12+1] + input_server[13+1] + input_server[14+1])

                if count == 22:
                    U_S_S_Scale_Variable = float(input_server[15+1] + input_server[16+1] + input_server[17+1])
                    line_tracking_module = int(input_server[18+1]), int(input_server[19+1]), int(input_server[20+1])
                elif count == 23:
                    U_S_S_Scale_Variable = float(input_server[15+1] + input_server[16+1] + input_server[17+1]
                                                 + input_server[18+1])
                    line_tracking_module = int(input_server[19+1]), int(input_server[20+1]), int(input_server[21+1])
                elif count == 24:
                    U_S_S_Scale_Variable = float(
                        input_server[15+1] + input_server[16+1] + input_server[17+1] + input_server[18+1]
                        + input_server[19+1])
                    line_tracking_module = int(input_server[20+1]), int(input_server[21+1]), int(input_server[22+1])
                elif count == 25:
                    U_S_S_Scale_Variable = float(input_server[15+1] + input_server[16+1] + input_server[17+1]
                                                 + input_server[18+1] + input_server[19+1] + input_server[20+1])
                    line_tracking_module = int(input_server[21+1]), int(input_server[22+1]), int(input_server[23+1])

                # change label etc.
                text_uss = str(U_S_S_Scale_Variable) + "cm"
                USS.configure(width=int(round(U_S_S_Scale_Variable)), text=text_uss)
                USS_Variable = float(U_S_S_Scale_Variable)

                if USS_Variable > 100:
                    USS.configure(bg="light blue", width=100)
                elif USS_Variable > 90:
                    USS.configure(bg="blue")
                elif USS_Variable > 50:
                    USS.configure(bg="green")
                elif USS_Variable > 25:
                    USS.configure(bg="orange")
                elif USS_Variable > 9:
                    USS.configure(bg="red")
                elif USS_Variable > 0:
                    USS.configure(bg="purple")

                if line_tracking_module[0]:
                    line_tracking_left.configure(bg="white")
                else:
                    line_tracking_left.configure(bg="black")

                if line_tracking_module[1]:
                    line_tracking_middle.configure(bg="white")
                else:
                    line_tracking_middle.configure(bg="black")

                if line_tracking_module[2]:
                    line_tracking_right.configure(bg="white")
                else:
                    line_tracking_right.configure(bg="black")
            except:
                pass
        elif "c" in input_server:
            cpu_temp_list = list(input_server)
            del(cpu_temp_list[0])
            cpu_temp_value = "".join(cpu_temp_list)
            cpu_temp.configure(text="Temperatur: " + cpu_temp_value + "°C")
        elif "b" in input_server:
            cpu_usage_list = list(input_server)
            del (cpu_usage_list[0])
            cpu_usage_value = "".join(cpu_usage_list)
            cpu_usage.configure(text="Usage: " + cpu_usage_value + "%")


'tkinter'
# main
main = tk.Tk()
main.title("Rasptank_Client_V2")
main.configure(bg="white")
main.geometry('3000x3000')

# Buttons
w = tk.Button(text="△", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
a = tk.Button(text="◁", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
d = tk.Button(text="▷", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
s = tk.Button(text="▽", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
arm_11_down = tk.Button(text="  ▽ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_11_up = tk.Button(text="  △ ", activebackground="grey", height=1, width=6, relief="groove",
                      bg="white", font=("calibri", 17))
arm_12_down = tk.Button(text="  ▽ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_12_up = tk.Button(text="  △ ", activebackground="grey", height=1, width=6, relief="groove",
                      bg="white", font=("calibri", 17))
arm_13_down = tk.Button(text="  ▽ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_13_up = tk.Button(text="  △ ", activebackground="grey", height=1, width=6, relief="groove",
                      bg="white", font=("calibri", 17))
arm_14_left = tk.Button(text="  ↺ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_14_right = tk.Button(text="  ↻ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))
arm_15_open = tk.Button(text=" ↤↦ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_15_close = tk.Button(text="  ↦↤ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))

w.place(x=200, y=201)
a.place(x=119, y=277)
d.place(x=281, y=277)
s.place(x=200, y=353)
arm_11_down.place(x=480, y=181)
arm_11_up.place(x=480, y=111)
arm_12_down.place(x=600, y=550)
arm_12_up.place(x=600, y=480)
arm_13_down.place(x=690, y=480)
arm_13_up.place(x=690, y=410)
arm_14_left.place(x=780, y=400)
arm_14_right.place(x=883, y=400)
arm_15_open.place(x=973, y=435)
arm_15_close.place(x=973, y=365)

# Lable
debug = tk.Label(bg="white", height=1, width=194, relief="sunken", borderwidth=3, background="#eeeeee", anchor="w",
                 text="Loading...")
linie1 = tk.Label(bg="white", height=1, width=100)

cpu_sign = tk.Label(text="CPU", bg="#efefef", relief="flat", height=2, width=19)
cpu_usage = tk.Label(text="Usage:  Loding...", bg="#efefef", relief="flat", height=1, width=19, anchor="w")
cpu_temp = tk.Label(text="Temperatur: Loding...", bg="#efefef", relief="flat", height=1, widt=19, anchor="w")

Ketten = tk.Label(text="Ketten", bg="#efefef", relief="flat", height=4, width=9)
arm_11 = tk.Label(text="        No.11        ", bg="#efefef", relief="flat")
arm_12 = tk.Label(text="        No.12        ", bg="#efefef", relief="flat")
arm_13 = tk.Label(text="        No.13        ", bg="#efefef", relief="flat")
arm_14 = tk.Label(text="No.\n14", bg="#efefef", relief="flat", height=3)
arm_15 = tk.Label(text="        No.15        ", bg="#efefef", relief="flat")

USS = tk.Label(bg="green", relief="flat", height=1, width=100, text="Loding...", anchor="e")
USS_sign = tk.Label(text="Ultrasonic-sensor", bg="#efefef", relief="flat")
USS_symbol = tk.Label(text="∘⪢", bg="#efefef", relief="flat")

line_tracking_sign = tk.Label(bg="light grey", height=1, width=33, text="Line Tracking Modul")
line_tracking_left = tk.Label(bg="grey", relief="flat", height=2, width=10)
line_tracking_middle = tk.Label(bg="grey", relief="flat", height=2, width=10)
line_tracking_right = tk.Label(bg="grey", relief="flat", height=2, width=10)

cpu_sign.place(x=1200, y=580)
cpu_usage.place(x=1200, y=620)
cpu_temp.place(x=1200, y=645)

Ketten.place(x=205, y=282)
arm_11.place(x=480, y=160)
arm_12.place(x=600, y=529)
arm_13.place(x=690, y=459)
arm_14.place(x=861, y=399)
arm_15.place(x=973, y=414)

USS.place(x=600, y=160)
USS_sign.place(x=600, y=139)
USS_symbol.place(x=580, y=160)

linie1.place(x=660, y=43)
debug.place(x=0, y=680)

line_tracking_sign.place(x=120, y=500)
line_tracking_right.place(x=280, y=525)
line_tracking_middle.place(x=200, y=525)
line_tracking_left.place(x=120, y=525)

'Steuerung'
# Buttons
for button in "w", "a", "s", "d":
    exec(button + ".bind('<ButtonPress-1>', " + button + "_press)")
    exec(button + ".bind('<ButtonRelease-1>', stop_every)")
for button in "arm_12_down", "arm_12_up", "arm_13_down", "arm_13_up", "arm_14_left", "arm_14_right", \
              "arm_15_open", "arm_15_close", "arm_11_down", "arm_11_up":
    exec(button + ".bind('<ButtonRelease-1>', stop_every)")

arm_11_down.bind('<ButtonPress-1>', arm_11_press_down)
arm_11_up.bind('<ButtonPress-1>', arm_11_press_up)
arm_12_down.bind('<ButtonPress-1>', arm_12_press_down)
arm_12_up.bind('<ButtonPress-1>', arm_12_press_up)
arm_13_down.bind('<ButtonPress-1>', arm_13_press_down)
arm_13_up.bind('<ButtonPress-1>', arm_13_press_up)
arm_14_left.bind('<ButtonPress-1>', arm_14_press_left)
arm_14_right.bind('<ButtonPress-1>', arm_14_press_right)
arm_15_close.bind('<ButtonPress-1>', arm_15_press_close)
arm_15_open.bind('<ButtonPress-1>', arm_15_press_open)

'Tastatursteuerung'
main.bind('<KeyPress>', key_press)
main.bind('<KeyRelease>', stop_every)

'Multiphread'
_thread.start_new_thread(uss_servo_cpu, ())

'mainloop'
main.mainloop()
