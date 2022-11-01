'INFOS'
'SOCKET'
# port : 1501


import tkinter
import tkinter.messagebox
import socket
import _thread
import time
import sys

# Variabeln
servo_11_position = 360
servo_12_position = 360
servo_13_position = 360
servo_14_position = 360
servo_15_position = 360
U_S_S_Scale_Variable = 0
counter1 = False
counter2 = "none"
every = "none"
event = 1

'Verbindung zum Server'
# Info
print("Verbinde zum Server...")
try:
    # Verbinung
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)
    server_addr = ('192.168.35.172', 1501)
    client.connect(server_addr)
    time.sleep(0.5)
    client.send(bytes("-VERBUNDEN-    -Test:2/3:OK", "utf8"))
    client.send(bytes("-VERBUNDEN-    -Test:3/3:OK", "utf8"))
    print("Mit Server Verbunden")
    time.sleep(0.5)
except:
    tkinter.messagebox.showerror("↑↓Verbindung",
                                 "Keine Verbindung Zum Server \n -Prüfe die Intenetverbindung \n -Prüfe ob der Server online ist")
    sys.exit()


# Funktionen
def uss_and_kamera():
    global U_S_S_Scale
    global servo_11_position
    global servo_12_position
    global servo_13_position
    global servo_14_position
    global servo_15_position
    global every
    while True:
        input_server = str(client.recv(1684), "utf8")
        if "a" in input_server:
            anzahl = len(input_server)
            print(input_server, "=>", anzahl)

            servo_11_position = int(input_server[0] + input_server[1] + input_server[2])
            servo_12_position = int(input_server[3] + input_server[4] + input_server[5])
            servo_13_position = int(input_server[6] + input_server[7] + input_server[6])
            servo_14_position = int(input_server[9] + input_server[10] + input_server[9])
            servo_15_position = int(input_server[12] + input_server[13] + input_server[14])
            if anzahl == 19:
                U_S_S_Scale_Variable = float(input_server[15] + input_server[16] + input_server[17] + input_server[18])
            elif anzahl == 20:
                U_S_S_Scale_Variable = float(
                    input_server[15] + input_server[16] + input_server[17] + input_server[18] + input_server[19])
            else:
                try:
                    U_S_S_Scale_Variable = float(input_server[15] + input_server[16])
                except:
                    pass
            U_S_S_Scale.set(U_S_S_Scale_Variable)

            print(servo_11_position)
            print(servo_12_position)
            print(servo_13_position)
            print(servo_14_position)
            print(servo_15_position)
            print(U_S_S_Scale_Variable)


def druck():
    global counter1
    global counter2
    counter1 = False
    counter2 = "none"
    print(counter2)
    while 1:
        client.send(bytes(counter2 + "-go", "utf8"))
        vorher = counter2
        print(counter2)
        while counter1:
            if vorher != counter2:
                pass
                client.send(bytes("Motor:stop", "utf8"))
                client.send(bytes(counter2 + "-go", "utf8"))
            counter1 = False
            time.sleep(0.1)
        client.send(bytes("Motor:stop", "utf8"))
        while not counter1:
            time.sleep(0.2)


# zwischenschritt-------------------
_thread.start_new_thread(druck, ())


# ----------------------------------


def w_(event):
    client.send(bytes("w-go", "utf8"))
    print("w")


def w_2(event):
    client.send(bytes("Motor:stop", "utf8"))
    print("Stop")


def a_(event):
    client.send(bytes("a-go", "utf8"))


def a_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def d_(event):
    client.send(bytes("d-go", "utf8"))


def d_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def s_(event):
    client.send(bytes("s-go", "utf8"))


def s_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def c_(event):
    client.send(bytes("c-go", "utf8"))


def c_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def f_(event):
    client.send(bytes("f-go", "utf8"))


def f_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def g_(event):
    client.send(bytes("g-go", "utf8"))


def g_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def z_(event):
    client.send(bytes("z-go", "utf8"))


def z_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def u_(event):
    client.send(bytes("u-go", "utf8"))


def u_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def i_(event):
    client.send(bytes("i-go", "utf8"))


def i_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def o_(event):
    client.send(bytes("o-go", "utf8"))


def o_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def p_(event):
    client.send(bytes("p-go", "utf8"))


def p_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def m_(event):
    client.send(bytes("m-go", "utf8"))


def m_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def k_(event):
    client.send(bytes("k-go", "utf8"))


def k_2(event):
    client.send(bytes("Motor:stop", "utf8"))


def uss(event):
    global U_S_S_Scale
    value = U_S_S_Scale.get()
    if value >= 90:
        U_S_S_Scale['troughcolor'] = 'green'
        U_S_S_Scale['fg'] = 'green'
    elif value >= 75:
        U_S_S_Scale['troughcolor'] = 'yellow'
        U_S_S_Scale['fg'] = 'yellow'
    elif value >= 50:
        U_S_S_Scale['troughcolor'] = '#ff8000'
        U_S_S_Scale['fg'] = '#ff8000'
    elif value >= 25:
        U_S_S_Scale['troughcolor'] = 'red'
        U_S_S_Scale['fg'] = 'red'
    elif value >= 10:
        U_S_S_Scale['troughcolor'] = 'dark red'
        U_S_S_Scale['fg'] = 'dark red'
    elif value >= 0:
        U_S_S_Scale['troughcolor'] = 'purple'
        U_S_S_Scale['fg'] = 'purple'


# Für die Tastenkombination___________________________________
def w__(w):
    global counter1
    global counter2
    counter1 = True
    counter2 = "w"


def a__(a):
    global counter1
    global counter2
    counter1 = True
    counter2 = "a"


def d__(d):
    global counter1
    global counter2
    counter1 = True
    counter2 = "d"


def s__(s):
    global counter1
    global counter2
    counter1 = True
    counter2 = "s"


def c__(c):
    global counter1
    global counter2
    counter1 = True
    counter2 = "c"


def f__(f):
    global counter1
    global counter2
    counter1 = True
    counter2 = "f"


def g__(g):
    global counter1
    global counter2
    counter1 = True
    counter2 = "g"


def z__(z):
    global counter1
    global counter2
    counter1 = True
    counter2 = "z"


def u__(u):
    global counter1
    global counter2
    counter1 = True
    counter2 = "u"


def i__(i):
    global counter1
    global counter2
    counter1 = True
    counter2 = "i"


def o__(o):
    global counter1
    global counter2
    counter1 = True
    counter2 = "o"


def p__(p):
    global counter1
    global counter2
    counter1 = True
    counter2 = "p"


def m__(m):
    global counter1
    global counter2
    counter1 = True
    counter2 = "m"


def k__(k):
    global counter1
    global counter2
    counter1 = True
    counter2 = "k"


# ___________________________________________________________

def exit_():
    exityesno = tkinter.messagebox.askyesno("Verlassen", "Wirklich Verlassen?")
    if exityesno:
        main.destroy()


# Klasse erstelle
main = tkinter.Tk()

# Name
main.title("Rasptank")

# Hintergrundfarbe ändern
main.configure(bg="#111010")

'Frame'
# Frame Erstellen

# Kamaera
bild = tkinter.Frame(height=20, width=30, bg="black")

# U-Schall-Sensor
uschallsensor = tkinter.Frame(bg="black", height=20, width=30, relief="sunken")

# Fames erscheinen lassen

# Bild
bild.grid(row=15, column=52)

# U-Schall-Sensor
uschallsensor.place(x=1000, y=200)

'Buttons'
# Buttons erstellen

# Exit
Exit = tkinter.Button(bg="black", fg="red", command=exit_, text="EXIT⛔", height=3, width=8,
                      activebackground="dark red")

# Ketten
d = tkinter.Button(text="->", fg="red", bg="black", width=8, height=3, activebackground="dark red")
a = tkinter.Button(text="<-", fg="red", bg="black", width=8, height=3, activebackground="dark red")
w = tkinter.Button(text="^", fg="red", bg="black", width=8, height=3, activebackground="dark red")
s = tkinter.Button(text="\/", fg="red", bg="black", width=8, height=3, activebackground="dark red")

# Roboter Arm

# Tastatur
# c = Motor Unten - Runter
# f = Motor Unten - Hoch
# g = 2. Motor - Runter
# z = 2. Motor - Hoch
# u = 3. Motor - Links Drehung
# i = 3. Motor - rechts Drehung
# 0 = 4. Motor - auf
# p = 4. Motor - zu
# k = kamera - hoch
# m = kamera -runter

f = tkinter.Button(command=f_, text="Hoch 🔼 \n -Motoer Unten", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")
c = tkinter.Button(command=c_, text="Runter 🔽 \n -Motor Unten", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")

z = tkinter.Button(command=z_, text="Hoch 🔼 /\ \n -2. Motor", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")
g = tkinter.Button(command=g_, text="Runter 🔽 \/ \n -2. Motoer", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")

u = tkinter.Button(command=u_, text="<-🔄 Links \n -3. Motor", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")
i = tkinter.Button(command=i_, text="Rechts 🔄->\n -3. Motor", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")

o = tkinter.Button(command=o_, text="Auf \n -4. Motor", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")
p = tkinter.Button(command=p_, text="Zu\n -4. Motor", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")

# Kamera
k = tkinter.Button(command=k_, text="Hoch🔼 \n -Kamera", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")
m = tkinter.Button(command=m_, text="Runter🔽 \n -Kamera", bg="black", fg="red", width=12, height=3,
                   activebackground="dark red")

# Buttons erscheinen lassen
# ______
# Benutzt:
# .grid
# row  /\  \/
# column <>
# ______

# Kettten
w.grid(row=29, column=50)
d.grid(row=30, column=51)
a.grid(row=30, column=49)
s.grid(row=30, column=50)

# Roboter Arm
# Zeile 295
f.grid(row=30, column=53)
c.grid(row=31, column=53)

g.grid(row=30, column=55)
z.grid(row=29, column=55)

u.grid(row=29, column=57)
i.grid(row=29, column=58)

o.grid(row=29, column=60)
p.grid(row=30, column=60)

# Kamera
m.place(x=847, y=112)
k.place(x=847, y=56)

# Exit
Exit.grid(row=1, column=49)

'Lable'
# Lable Erstellen

# Abstand
abstand = tkinter.Label(height=1, width=1, bg="#111010", fg="#111010", text="-")
abstand2 = tkinter.Label(height=1, width=1, bg="#111010", fg="#111010", text="-")
abstand3 = tkinter.Label(height=1, width=1, bg="#111010", fg="#111010", text="-")
abstand4 = tkinter.Label(height=1, width=1, bg="#111010", fg="#111010", text="")

# Name
bild_name = tkinter.Label(text="Live Video Übertragung", height=1, width=25, bg="black", fg="red", relief="groove")
U_Schall_Sensor_Name = tkinter.Label(text="Ultra-Schall-Sensor", bg="black", fg="red", highlightcolor="red")

# Später weg
bild_lable = tkinter.Label(text="--KEIN VIDEO--", height=30, width=90, bg="#131313", master=bild)

# Lable erscheinen lassen
# Name
bild_name.grid(row=16, column=52)
U_Schall_Sensor_Name.place(x=1100, y=178.5)

# Abstand
abstand.grid(row=30, column=54)
abstand2.grid(row=29, column=56)
abstand3.grid(row=29, column=59)
abstand4.grid(row=1, column=1)

# Später weg
bild_lable.grid(row=1, column=1)

'Skalen'
# Skalen erstellen
U_S_S_Scale = tkinter.Scale(variable=U_S_S_Scale_Variable, bg="black", fg="red", master=uschallsensor,
                            sliderlength=10, from_=float(0.00), to=float(100.00), tickinterval=float(50.00),
                            troughcolor="red", width=20, orient="horizontal", length=300,
                            highlightbackground="#010101", highlightcolor="#010101", borderwidth=3, command=uss)
U_S_S_Scale["activebackground"] = "red"
U_S_S_Scale.set(100)

# Skalen erscheine lassen
U_S_S_Scale.pack()

'Tastatur Steuerung'
main.bind("<w>", func=w__)
main.bind("<a>", func=a__)
main.bind("<d>", func=d__)
main.bind("<s>", func=s__)
main.bind("<c>", func=c__)
main.bind("<f>", func=f__)
main.bind("<g>", func=g__)
main.bind("<z>", func=z__)
main.bind("<u>", func=u__)
main.bind("<i>", func=i__)
main.bind("<o>", func=o__)
main.bind("<p>", func=p__)
main.bind("<m>", func=m__)
main.bind("<k>", func=k__)

'Button - realse<->Press'
for buttonn in "w", "a", "s", "d", "c", "f", "g", "z", "u", "i", "o", "p", "k", "m":
    exec(buttonn + ".bind('<ButtonPress-1>', " + buttonn + "_)")
    exec(buttonn + ".bind('<ButtonRelease-1>', " + buttonn + "_2)")

'Mutiphread'
# U_S_S
_thread.start_new_thread(uss_and_kamera, ())

main.mainloop()
