import tkinter as tk
from tkinter import*
import RPi.GPIO as GPIO
import time
from threading import Thread
import spidev


digitalInputList = {}
digitalInputList['DI_INPUT_TAKO'] = 23



global tako
global flag
global tako2
tako = 0
flag=False
pinState = {}


form=tk.Tk()
form.title("TAKO SAYMA")
form.geometry("600x300+50+100")

def __initGPIO__():
    print("__initGPIO__")
    global spi
    spi = spidev.SpiDev()    
    GPIO.setmode(GPIO.BCM)
    for key, value in digitalInputList.items():
        GPIO.setup(digitalInputList[key], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        pinState[key] = 1
        print("pin -->> ", key, str(value))
      
def getDIVal(ch, key):
    if not GPIO.input(ch):
        return False
    else:
        return True 
    
def yaz():
    entry.delete(0,tk.END)
    entry.insert(0,tako)

def reset():
    entry.delete(0,tk.END)
def resetTako():
    global tako
    tako=0
    entry.delete(0,tk.END)
    
def Kaydet():
    file=open('pulse.txt','a')
    file.write(entry.get()+",")
    
   
def digitalInputListener():    
    global tako    
    while 1:
        for key, value in digitalInputList.items():
            if getDIVal(value, key):
                if pinState[key] == 0:
                    pinState[key] = 1           
                    #takodan sinyal geldiyse => GPIO_23 BTN_TAKO
                    if value == digitalInputList['DI_INPUT_TAKO']:                        
                        tako += 1
                        tako2 = tako
            elif pinState[key] == 1:
                pinState[key] = 0
                
        time.sleep(0.0001)    



button=tk.Button(form,text="PRİNT_TAKO",height=3,width=10,command=yaz)
button.pack(side=tk.RIGHT)


button=tk.Button(form,text="RESET_TAKO",height=3,width=10,command=resetTako)
button.pack(side=tk.LEFT)

button=tk.Button(form,text="SAVE_TEXT",height=3,width=10,command=Kaydet)
button.pack(side=tk.LEFT)



entry=tk.Entry(form,width="20",font="Arial 30 bold")
entry.pack(side=tk.TOP)

form.mainloop
__initGPIO__()


t1=Thread(target=digitalInputListener)
t1.start()

  
        
        




