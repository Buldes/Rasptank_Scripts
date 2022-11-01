"""System Infos"""
'Imports'
import psutil
import os

'Definitions'


# CPU
def cpu_statistic():
    if os.name == "posix":
        cpu_temp_every = str(psutil.sensors_temperatures())
        cpu_temp = cpu_temp_every[42] + cpu_temp_every[43] + cpu_temp_every[44] + cpu_temp_every[45] + \
                   cpu_temp_every[46]
        cpu_usage = str(psutil.cpu_percent())
        return cpu_usage, cpu_temp
    else:
        cpu_usage = str(psutil.cpu_percent())
        return cpu_usage


# Memory
def memory_statics(to_GB=True, round_num=1):
    memory = psutil.virtual_memory()
    if to_GB:
        available = round(memory.available / 1024.0 / 1024.0 / 1024.0, round_num)
        total = round(memory.total / 1024.0 / 1024.0 / 1024.0, round_num)
    else:
        available = round(memory.available, round_num)
        total = round(memory.total, round_num)
    return available, total


# disk
def disk_statistics(to_GB=True, round_num=1):
    disk = psutil.disk_usage("/")
    if to_GB:
        free = round(disk.free / 1024.0 / 1024.0 / 1024, round_num)
        total = round(disk.total / 1024.0 / 1024.0 / 1024, round_num)
    else:
        free = round(disk.free, round_num)
        total = round(disk.total, round_num)
    return free, total


def info():
    print("************************************** \n"
          "             -sys_info-             \n"
          "disk_statistic(to_GB, round_num):\n"
          "   return list (free, total)\n"
          "    of disk\n"
          "\n"
          "memory_statistic(to_GB, round_num):\n"
          "   return list (available, total)\n"
          "    of memory\n"
          "\n"
          "cpu_statistic():\n"
          "   return list (usage in %, temperature)\n"
          "\n"
          "to_GB:\n"
          "   converts to GB\n"
          "\n"
          "round_num:\n"
          "   round the number\n"
          "**************************************")


if __name__ == '__main__':
    'Windows'
    if os.name == 'nt':
        import tkinter as tk
        import _thread
        import time

        # Frame erstellen
        main = tk.Tk()
        main.title("Statistic")
        main.configure(bg="#000000")


        def config():
            while 1:
                time.sleep(0.5)
                cpu_lable.configure(text="CPU: " + str(cpu_statistic()) + "%")
                memory.configure(
                    text="MEMORY: " + str(round(memory_statics()[0], 1)) + " / " + str(
                        memory_statics()[1]) + "GB")
                disk.configure(text="DISK: " + str(disk_statistics()[0]) + " / " + str(disk_statistics()[1]) + "GB")


        # Lable
        sys_info = tk.Label(bg="#090909", width=20, height=2, fg="#ffffff", text="-sys_info-", font=10)
        sys_info.pack()

        cpu_lable = tk.Label(bg="#0a0a0a")
        cpu_lable.configure(width=25, height=2, fg="#ffffff", text="Load...")
        cpu_lable.pack()

        memory = tk.Label(bg="#0a0a0a")
        memory.configure(width=25, height=2, fg="#ffffff", text="Load...")
        memory.pack()

        disk = tk.Label(bg="#0a0a0a")
        disk.configure(width=25, height=2, fg="#ffffff", text="Load...")
        disk.pack()

        _thread.start_new_thread(config, ())

        main.mainloop()

    if os.name == 'posix':
        import time

        info()
        time.sleep(0.5)
        while True:
            print("---------sys_info---------")
            print("cpu_usage:", cpu_statistic()[0], "%")
            print("cpu_temp:", cpu_statistic()[1], "°C")
            print("memory:" + str(memory_statics()[0]) + "/" + str(memory_statics()[1]))
            print("disk:" + str(disk_statistics()[0]) + "/" + str(disk_statistics()[1]))
            print("--------------------------")
            time.sleep(1)
