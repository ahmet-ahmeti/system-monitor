import psutil
import time
import os

#just to make a loop that never ends so it always checks for changes
while True: 

    os.system("clear")

    processes = []

    #adds processes name and usage percentage to a list
    for proc in psutil.process_iter(["name", "cpu_percent"]):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            pass

    #adds the processes that are not None to this lists then sorts it form most usage to least from the key also only adds the top 5        
    top5 = sorted([prog for prog in processes if prog["cpu_percent"] is not None], key=lambda x: x["cpu_percent"], reverse=True)[:5] 

    #checks usage of the disk on that path or directory /System/Volumes/Data is where youll find APFS(Apple's file system)
    #which has a seperate container from the normal path
    disk = psutil.disk_usage('/System/Volumes/Data') 

    #cheks the cpu usage for 1 sec then returns a precentage
    cpu = psutil.cpu_percent(interval=1) 
    ram = psutil.virtual_memory()

    print(f"CPU: {cpu:.1f}%")

    #1024 to the power of three to turn bytes to GB
    print(f"RAM: {ram.used / (1024**3):.1f}GB / {ram.total / (1024**3):.1f}GB ({ram.percent}%)") 

    #same as the one before
    print(f"DISK: {disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB ({disk.percent}%)") 
    print("\n")
    print("Top 5 processes:")
    for prog in top5:
        print(f"{prog['name']:<25} {prog['cpu_percent']:.1f}%") 

    #5 second pause between loops
    time.sleep(5) 

