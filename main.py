#########################################################  
import serial
from time import sleep
import threading
import tkinter as tk
import csv
from PSU import *
from serial_control import *
from valves import *
#########################################################

def sputterThread():
    global isRunning
    global delay
    global HEIGHT
    global WIDTH
    global isRFOn
    while isRunning==True:
        GetControl()
        root = tk.Tk()
        canvas=tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        
        buttonFrame=tk.Frame(root, bg="black", bd=10)
        buttonFrame.place(relx = 0.01,rely=0.01, relwidth=0.6, relheight=0.98)        
        button1 = tk.Button(buttonFrame, text="Guided Sputtering [WIP]", fg='white', bg='grey')
        button1.grid(row=0, column=0, columnspan=3, ipadx=70)
        
        label2 = tk.Label(buttonFrame, text="Set Power [0-100W]", fg='white', bg='black')
        label2.grid(row=1, column=0)
        entry2=tk.Entry(buttonFrame, bg='grey')
        entry2.grid(row=1, column=1)
        button2=tk.Button(buttonFrame, text="Confirm", fg='white', bg='grey', command=lambda: SetPower(entry2.get()))
        button2.grid(row=1, column=2)
        
        label3 = tk.Label(buttonFrame, text="Activate RF", fg='white', bg='black')
        label3.grid(row=2, column=0)
        button3=tk.Button(buttonFrame, text="Activate", fg='white', bg='grey', command=lambda: ActivateRF())
        button3.grid(row=2, column=1)
        label4 = tk.Label(buttonFrame, text="Deactviate RF", fg='white', bg='black')
        label4.grid(row=2, column=2)
        button4=tk.Button(buttonFrame, text="Deactviate", fg='white', bg='grey', command=lambda: DeactivateRF())
        button4.grid(row=2, column=3)
        
        label4 = tk.Label(buttonFrame, text="Open Valves (>6 seconds)", fg='white', bg='black')
        label4.grid(row=3, column=0)
        entry4=tk.Entry(buttonFrame, bg='grey')
        entry4.grid(row=3, column=1)
        label42 = tk.Label(buttonFrame, text="Gun Select (1 or 2)", fg='white', bg='black')
        label42.grid(row=4, column=0)
        entry42=tk.Entry(buttonFrame, bg='grey')
        entry42.grid(row=4, column=1)
        button4=tk.Button(buttonFrame, text="Confirm", fg='white', bg='grey', command=lambda: threading.Thread(openValvesfor(int(entry42.get()), int(entry4.get()))))
        button4.grid(row=3, column=2, rowspan=2)
                
        root.mainloop()
        isRunning=False
    return

def main():
    tryToOpenPSUPort()
    ArduinoUnoSerial = serial.Serial('/dev/ttyACM0', 9600) 
    isRunning=True
    delay=0.5 #donotchange
    HEIGHT=400
    WIDTH=800
    isRFOn=False
    isSputtering=False
    forwardPower=0
    reversePower=0
    loadPower=0
    sputter = threading.Thread(target=sputterThread)
    sputter.start()

    while isRunning==True:
        pingOnce()
        print("ping")
        sleep(0.7)
        if isRFOn==True:
            forwardPower, reversePower, loadPower=GetPower()
            if isSputtering:
                if loadPower==0:
                    DeactivateRF()
                    print("PSU Shorted, please wait for timer to finish before continuing")
            with open('power.csv', 'w', newline='') as f:
                thewriter=csv.writer(f)
                forwardPower, reversePower, loadPower=GetPower()
                thewriter.writerow([forwardPower, reversePower, loadPower])

    ArduinoUnoSerial.close()
    ser.close()
