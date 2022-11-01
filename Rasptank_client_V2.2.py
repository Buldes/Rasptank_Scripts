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

        # ip_addr =  '192.168.178.31'   # WLan
        ip_addr = '192.168.113.172'  # Hotspot

        client.connect((ip_addr, 1501))
        time.sleep(0.2)
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
speed = 70
status_press = "none"
line_tracking_module = "none"

arm_11_position = 360
arm_12_position = 360
arm_13_position = 360
arm_14_position = 360
arm_15_position = 360
pressed_key = dict(w=False, a=False, s=False, d=False, c=False, f=False, g=False, z=False, u=False, i=False,
                   o=False, p=False, k=False, m=False)
key = "none"

'Definition'


def w_press(event):
    global pressed_key
    if pressed_key["w"]:
        pressed_key["w"] = False
    else:
        pressed_key["w"] = True


def a_press(event):
    global pressed_key
    if pressed_key["a"]:
        pressed_key["a"] = False
    else:
        pressed_key["a"] = True


def s_press(event):
    global pressed_key
    if pressed_key["s"]:
        pressed_key["s"] = False
    else:
        pressed_key["s"] = True


def d_press(event):
    global pressed_key
    if pressed_key["d"]:
        pressed_key["d"] = False
    else:
        pressed_key["d"] = True


def arm_11_press_plus(event):
    global pressed_key
    if pressed_key["k"]:
        pressed_key["k"] = False
    else:
        pressed_key["k"] = True


def arm_12_press_plus(event):
    global pressed_key
    if pressed_key["f"]:
        pressed_key["f"] = False
    else:
        pressed_key["f"] = True


def arm_13_press_plus(event):
    global pressed_key
    if pressed_key["z"]:
        pressed_key["z"] = False
    else:
        pressed_key["z"] = True


def arm_14_press_plus(event):
    global pressed_key
    if pressed_key["i"]:
        pressed_key["i"] = False
    else:
        pressed_key["i"] = True


def arm_15_press_plus(event):
    global pressed_key
    if pressed_key["p"]:
        pressed_key["p"] = False
    else:
        pressed_key["p"] = True


def arm_11_press_minus(event):
    global pressed_key
    if pressed_key["m"]:
        pressed_key["m"] = False
    else:
        pressed_key["m"] = True


def arm_12_press_minus(event):
    global pressed_key
    if pressed_key["c"]:
        pressed_key["c"] = False
    else:
        pressed_key["c"] = True


def arm_13_press_minus(event):
    global pressed_key
    if pressed_key["g"]:
        pressed_key["g"] = False
    else:
        pressed_key["g"] = True


def arm_14_press_minus(event):
    global pressed_key
    if pressed_key["u"]:
        pressed_key["u"] = False
    else:
        pressed_key["u"] = True


def arm_15_press_minus(event):
    global pressed_key
    if pressed_key["o"]:
        pressed_key["o"] = False
    else:
        pressed_key["o"] = True


def key_press(event):
    global key
    key = str(event)

    if "'w'" in key:
        pressed_key["w"] = True
    elif "'d'" in key:
        pressed_key["d"] = True
    elif "'s'" in key:
        pressed_key["s"] = True
    elif "'a'" in key:
        pressed_key["a"] = True
    elif "'c'" in key:
        pressed_key["c"] = True
    elif "'f'" in key:
        pressed_key["f"] = True
    elif "'g'" in key:
        pressed_key["g"] = True
    elif "'z'" in key:
        pressed_key["z"] = True
    elif "'i'" in key:
        pressed_key["i"] = True
    elif "'u'" in key:
        pressed_key["u"] = True
    elif "'o'" in key:
        pressed_key["o"] = True
    elif "'p'" in key:
        pressed_key["p"] = True
    elif "'k'" in key:
        pressed_key["k"] = True
    elif "'m'" in key:
        pressed_key["m"] = True

    if "'w'" in key and "KeyRelease" in key:
        pressed_key["w"] = False
    elif "'d'" in key and "KeyRelease" in key:
        pressed_key["d"] = False
    elif "'s'" in key and "KeyRelease" in key:
        pressed_key["s"] = False
    elif "'a'" in key and "KeyRelease" in key:
        pressed_key["a"] = False
    elif "'c'" in key and "KeyRelease" in key:
        pressed_key["c"] = False
    elif "'f'" in key and "KeyRelease" in key:
        pressed_key["f"] = False
    elif "'g'" in key and "KeyRelease" in key:
        pressed_key["g"] = False
    elif "'z'" in key and "KeyRelease" in key:
        pressed_key["z"] = False
    elif "'i'" in key and "KeyRelease" in key:
        pressed_key["i"] = False
    elif "'u'" in key and "KeyRelease" in key:
        pressed_key["u"] = False
    elif "'o'" in key and "KeyRelease" in key:
        pressed_key["o"] = False
    elif "'p'" in key and "KeyRelease" in key:
        pressed_key["p"] = False
    elif "'k'" in key and "KeyRelease" in key:
        pressed_key["k"] = False
    elif "'m'" in key and "KeyRelease" in key:
        pressed_key["m"] = False


def send_data():
    global pressed_key
    pressed_key_past = pressed_key.copy()
    next_copy = False

    while True:
        for key_key in pressed_key:
            if pressed_key[key_key] != pressed_key_past[key_key]:
                next_copy = True
                if pressed_key[key_key]:
                    client.send(bytes(str(key_key) + "-press", "UTF8"))
                else:
                    client.send(bytes(str(key_key) + "-release", "UTF8"))
        if next_copy:
            pressed_key_past = pressed_key.copy()
            next_copy = False


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
                arm_11_position = int(input_server[0 + 1] + input_server[1 + 1] + input_server[2 + 1])
                arm_12_position = int(input_server[3 + 1] + input_server[4 + 1] + input_server[5 + 1])
                arm_13_position = int(input_server[6 + 1] + input_server[7 + 1] + input_server[6 + 1])
                arm_14_position = int(input_server[9 + 1] + input_server[10 + 1] + input_server[9 + 1])
                arm_15_position = int(input_server[12 + 1] + input_server[13 + 1] + input_server[14 + 1])

                if count == 22:
                    U_S_S_Scale_Variable = float(input_server[15 + 1] + input_server[16 + 1] + input_server[17 + 1])
                    line_tracking_module = int(input_server[18 + 1]), int(input_server[19 + 1]), int(
                        input_server[20 + 1])
                elif count == 23:
                    U_S_S_Scale_Variable = float(input_server[15 + 1] + input_server[16 + 1] + input_server[17 + 1]
                                                 + input_server[18 + 1])
                    line_tracking_module = int(input_server[19 + 1]), int(input_server[20 + 1]), int(
                        input_server[21 + 1])
                elif count == 24:
                    U_S_S_Scale_Variable = float(
                        input_server[15 + 1] + input_server[16 + 1] + input_server[17 + 1] + input_server[18 + 1]
                        + input_server[19 + 1])
                    line_tracking_module = int(input_server[20 + 1]), int(input_server[21 + 1]), int(
                        input_server[22 + 1])
                elif count == 25:
                    U_S_S_Scale_Variable = float(input_server[15 + 1] + input_server[16 + 1] + input_server[17 + 1]
                                                 + input_server[18 + 1] + input_server[19 + 1] + input_server[20 + 1])
                    line_tracking_module = int(input_server[21 + 1]), int(input_server[22 + 1]), int(
                        input_server[23 + 1])

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

                if not line_tracking_module[2]:
                    line_tracking_left.configure(bg="white")
                else:
                    line_tracking_left.configure(bg="black")

                if not line_tracking_module[1]:
                    line_tracking_middle.configure(bg="white")
                else:
                    line_tracking_middle.configure(bg="black")

                if not line_tracking_module[0]:
                    line_tracking_right.configure(bg="white")
                else:
                    line_tracking_right.configure(bg="black")
            except:
                pass
        elif "c" in input_server:
            cpu_temp_list = list(input_server)
            del (cpu_temp_list[0])
            cpu_temp_value = "".join(cpu_temp_list)
            cpu_temp.configure(text="Temperatur: " + cpu_temp_value + "°C")
        elif "b" in input_server:
            cpu_usage_list = list(input_server)
            del (cpu_usage_list[0])
            cpu_usage_value = "".join(cpu_usage_list)
            cpu_usage.configure(text="Benutzung: " + cpu_usage_value + "%")


'tkinter'
# main
main = tk.Tk()
main.title("Rasptank_Client_V2.2")
main.configure(bg="#ffffff")
main.geometry("1920x1080")

# BG
bg = tk.PhotoImage(file="bg.gif")
canvas1 = tk.Canvas(main, width=400, height=100, bg="#ffffff")
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

# Buttons
w = tk.Button(text="△", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
a = tk.Button(text="◁", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
d = tk.Button(text="▷", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))
s = tk.Button(text="▽", activebackground="grey", height=2, width=6, relief="groove", bg="white", font=("calibri", 17))

arm_11_plus = tk.Button(text="  ▽ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_11_minus = tk.Button(text="  △ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))
arm_12_minus = tk.Button(text="  ▽ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))
arm_12_plus = tk.Button(text="  △ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_13_minus = tk.Button(text="  ▽ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))
arm_13_plus = tk.Button(text="  △ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_14_minus = tk.Button(text="  ↺ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))
arm_14_plus = tk.Button(text="  ↻ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))
arm_15_minus = tk.Button(text=" ↤↦ ", activebackground="grey", height=1, width=6, relief="groove",
                         bg="white", font=("calibri", 17))
arm_15_plus = tk.Button(text="  ↦↤ ", activebackground="grey", height=1, width=6, relief="groove",
                        bg="white", font=("calibri", 17))

w.place(x=200, y=201)
a.place(x=119, y=277)
d.place(x=281, y=277)
s.place(x=200, y=353)
arm_11_plus.place(x=480, y=181)
arm_11_minus.place(x=480, y=111)
arm_12_minus.place(x=600, y=550)
arm_12_plus.place(x=600, y=480)
arm_13_minus.place(x=690, y=480)
arm_13_plus.place(x=690, y=410)
arm_14_minus.place(x=780, y=400)
arm_14_plus.place(x=883, y=400)
arm_15_minus.place(x=973, y=435)
arm_15_plus.place(x=973, y=365)

# Lable
cpu_sign = tk.Label(text="CPU", bg="#afafaf", relief="flat", height=2, width=19)
cpu_usage = tk.Label(text="Benutzung:  Lade...", bg="#efefef", relief="flat", height=1, width=19, anchor="w")
cpu_temp = tk.Label(text="Temperatur: Lade...", bg="#efefef", relief="flat", height=1, widt=19, anchor="w")

Ketten = tk.Label(text="Ketten", bg="#efefef", relief="flat", height=4, width=9)
arm_11 = tk.Label(text="        Nr.11        ", bg="#efefef", relief="flat")
arm_12 = tk.Label(text="        Nr.12        ", bg="#efefef", relief="flat")
arm_13 = tk.Label(text="        Nr.13        ", bg="#efefef", relief="flat")
arm_14 = tk.Label(text="Nr.\n14", bg="#efefef", relief="flat", height=3)
arm_15 = tk.Label(text="        Nr.15        ", bg="#efefef", relief="flat")

USS = tk.Label(bg="green", relief="flat", height=1, width=100, text="Lade...", anchor="e")
USS_sign = tk.Label(text="Ultraschallsensor", bg="#efefef", relief="flat")
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

line_tracking_sign.place(x=120, y=500)
line_tracking_right.place(x=280, y=525)
line_tracking_middle.place(x=200, y=525)
line_tracking_left.place(x=120, y=525)

'Steuerung'
for button in range(11, 16):
    exec("arm_" + str(button) + "_minus.bind('<ButtonPress-1>', arm_" + str(button) + "_press_minus)")
    exec("arm_" + str(button) + "_minus.bind('<ButtonRelease-1>', arm_" + str(button) + "_press_minus)")
for button in range(11, 16):
    exec("arm_" + str(button) + "_plus.bind('<ButtonPress-1>', arm_" + str(button) + "_press_plus)")
    exec("arm_" + str(button) + "_plus.bind('<ButtonRelease-1>', arm_" + str(button) + "_press_plus)")
for button in "w", "a", "s", "d":
    exec(button + ".bind('<ButtonPress-1>', " + button + "_press)")
    exec(button + ".bind('<ButtonRelease-1>', " + button + "_press)")

'Tastatursteuerung'
main.bind('<KeyPress>', key_press)
main.bind('<KeyRelease>', key_press)

'Multiphread'
_thread.start_new_thread(uss_servo_cpu, ())
_thread.start_new_thread(send_data, ())

'mainloop'
main.mainloop()
