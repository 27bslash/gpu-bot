import os
import time
import datetime
import win32api


def shutdown():
    now = datetime.datetime.now().time()
    shutoff_time = datetime.time(4, 15, 0)
    max_shutoff = datetime.time(6, 0, 0)
    if now > shutoff_time and now < max_shutoff and idle_checker() > 600:
        os.system('shutdown -s')

def idle_checker():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


