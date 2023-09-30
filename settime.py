# datetime.py
from ntptime import settime
from utime import localtime
from utime import time
from machine import RTC
def set_time():
    print("\nTime being calibrated...")
    settime()
    rtc=RTC()
    tampon1=time() 
    tampon2=tampon1+28800
    rtc.datetime (localtime(tampon2)[0:3]+(0,)+localtime(tampon2)[3:6] + (0,))
    print("OK!\n")

def date_now():
    a = localtime()
    print(str(a[0])+'-'+str(a[1])+'-'+str(a[2]))
    
def time_now():
    a = localtime()
    print(str(a[3])+':'+str(a[4])+':'+str(a[5])+'\n')