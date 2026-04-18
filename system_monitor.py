import psutil
from tkinter import *
import os

window = Tk()

window.title("System Monitor")

window.config(background="#303030")

# Baseline call so the first cpu_percent() reading isn't 0.0
psutil.cpu_percent(interval=None)

# to check for os cause you need different file path depending on OS
if os.name == "nt":
    disk_path = "C:\\"
elif os.name == "posix":
    if os.uname().sysname == "Darwin":
        disk_path = "/System/Volumes/Data"
    elif os.uname().sysname == "Linux":
        disk_path = "/"

def on_enter(e):
    e.widget.config(background="#505050")


def on_leave(e):
    e.widget.config(background="#303030")


cpu_label = Label(window, text="CPU: ", font=("Monaco", 30), background="#303030", cursor="pointinghand", width=32, height="2")
cpu_label.bind("<Enter>", on_enter)
cpu_label.bind("<Leave>", on_leave)
cpu_label.pack(padx=40, pady=15)

ram_label = Label(window, text="RAM: ", font=("Monaco", 30), background="#303030", cursor="pointinghand", width=32, height="2")
ram_label.bind("<Enter>", on_enter)
ram_label.bind("<Leave>", on_leave)
ram_label.pack(padx=40, pady=2)

disk_label = Label(window, text="DISK: ", font=("Monaco", 30), background="#303030", cursor="pointinghand", width=32, height="2")
disk_label.bind("<Enter>", on_enter)
disk_label.bind("<Leave>", on_leave)
disk_label.pack(padx=40, pady=2)

top_5_label = Label(window, text="", font=("Monaco", 25), background="#303030", cursor="pointinghand", justify="left", width=35, height=8)
top_5_label.bind("<Enter>", on_enter)
top_5_label.bind("<Leave>", on_leave)
top_5_label.pack(pady=15)

def main():

    processes = []

    # adds processes name and usage percentage to a list
    for proc in psutil.process_iter(["name", "cpu_percent"]):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            pass


    # removing programs that are using None % and the System Idle Process for Windows         
    top5 = sorted([prog for prog in processes if prog["cpu_percent"] is not None and prog["name"] != "System Idle Process"], key=lambda x: x["cpu_percent"], reverse=True)[:5] 


    disk = psutil.disk_usage(disk_path) 

    # None cause it uses the 2 second pause between loops
    cpu = psutil.cpu_percent(interval=None) 
    ram = psutil.virtual_memory()


    top5_text = "\n\nTop 5 processes by CPU:\n"
    for prog in top5:
        top5_text += f"{prog['name']:<25} {prog['cpu_percent']:.1f}%\n"




    # 1024 to the power of three to turn bytes to GB
    cpu_label.config(text=(f"CPU: {cpu:.1f}%"))

    ram_label.config(text=(f"RAM: {ram.used / (1024**3):.1f}GB / {ram.total / (1024**3):.1f}GB ({ram.percent}%)"))

    disk_label.config(text=(f"DISK: {disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB ({disk.percent}%)"))

    top_5_label.config(text=(top5_text))


    window.after(2000, main)

main()

window.mainloop()
