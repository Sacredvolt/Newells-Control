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
def GenerateCommand(CMDID, PARM1, PARM2):
    HEAD='43'
    ADDR='01'
    command=bytearray.fromhex(HEAD+ADDR+CMDID+PARM1+PARM2)
    CKSUM=0
    for i in command:       #spits out CKSUM in decimal as integer
        CKSUM=CKSUM+i
    CKSUM=CKSUM.to_bytes(2, 'big')      #converts integer CHKSUM to 2-byte hex, high byte first (big)
    command=command+CKSUM #appends 2-byte CHKSUM to command
    return command

def SendCommand(command):
    ser.write(command)
    reading=ser.read(50)
    return reading

def GenAndSend(CMDID, PARM1, PARM2):
    command=GenerateCommand(CMDID, PARM1, PARM2)
    reading=SendCommand(command)
    return reading

def pingOnce():
    replyPing=GenAndSend('4250','0000','0000')
    return replyPing
        
def GetControl():
    reply=GenAndSend('4243','5555','0000')
    print(reply.hex())
    return reply

def RelControl():
    reply=GenAndSend('4243','0000','0000')
    print(reply.hex())
    return reply

def GetPower():
    reply=GenAndSend('4750','0000','0000')
    reply=reply[5:-2]
    forwardPower=reply[:2]
    reversePower=reply[2:4]
    loadPower=reply[4:]
    print(forwardPower, reversePower, loadPower)
    return forwardPower, reversePower, loadPower

def SetPower(desiredPower):
    desiredPower=int(desiredPower)
    desiredPower=desiredPower.to_bytes(2,'big')
    HEAD='43'
    ADDR='01'
    CMDID='5341'
    CKSUM=0
    command1=bytearray.fromhex(HEAD+ADDR+CMDID)
    command2=bytearray.fromhex('0000')
    command=command1+desiredPower+command2
    for i in command:       #spits out CKSUM in decimal as integer
        CKSUM=CKSUM+i
    CKSUM=CKSUM.to_bytes(2, 'big')      #converts integer CHKSUM to 2-byte hex, high byte first (big)
    command=command+CKSUM #appends 2-byte CHKSUM to command
    reply=SendCommand(command)
    return reply

def setTunerAuto():
    return GenAndSend('544D', '0001', '0000')

def setTunerManual():
    return GenAndSend('544D', '0002', '0000')

def setLoadTunerCapPosition():
    desiredLoad=int(30)
    desiredLoad=desiredLoad.to_bytes(2,'big')
    HEAD='43'
    ADDR='01'
    CMDID='5443'
    CKSUM=0
    command1=bytearray.fromhex(HEAD+ADDR+CMDID)
    command2=bytearray.fromhex('0001')
    command=command1+command2+desiredLoad
    for i in command:       #spits out CKSUM in decimal as integer
        CKSUM=CKSUM+i
    CKSUM=CKSUM.to_bytes(2, 'big')      #converts integer CHKSUM to 2-byte hex, high byte first (big)
    command=command+CKSUM #appends 2-byte CHKSUM to command
    reply=SendCommand(command)   
    return reply

def setTuneTunerCapPosition():
    desiredTune=int(70)
    desiredTune=desiredTune.to_bytes(2,'big')
    HEAD='43'
    ADDR='01'
    CMDID='5443'
    CKSUM=0
    command1=bytearray.fromhex(HEAD+ADDR+CMDID)
    command2=bytearray.fromhex('0002')
    command=command1+command2+desiredTune
    for i in command:       #spits out CKSUM in decimal as integer
        CKSUM=CKSUM+i
    CKSUM=CKSUM.to_bytes(2, 'big')      #converts integer CHKSUM to 2-byte hex, high byte first (big)
    command=command+CKSUM #appends 2-byte CHKSUM to command
    reply=SendCommand(command)   
    return reply

def autoSetTunerCaps():
    setTunerManual()
    sleep(0.1)
    setLoadTunerCapPosition()
    sleep(0.1)
    setTuneTunerCapPosition()
    sleep(0.1)
    setTunerAuto()
    sleep(0.1)
    return

def ActivateRF():
    global isRFOn
    setTunerManual()
    sleep(0.1)
    setLoadTunerCapPosition()
    sleep(0.1)
    setTuneTunerCapPosition()
    sleep(0.1)
    setTunerAuto()
    sleep(0.1)
    reply=GenAndSend('4252','5555','0000')
    isRFOn=True
    return reply

def DeactivateRF():
    global isRFOn
    reply=GenAndSend('4252','0000','0000')
    isRFOn=False
    return reply


def sputterThread():
    global isRunning
    global delay
    global HEIGHT
    global WIDTH
    global isRFOn
    global percentageDone
    
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
        button4=tk.Button(buttonFrame, text="Confirm", fg='white', bg='grey', command=lambda:threading.Thread(openValvesfor(int(entry42.get()), int(entry4.get()))))
        button4.grid(row=3, column=2, rowspan=2)
                
        root.mainloop()
        isRunning=False
    return

def main():
    global ser
    global isRunning
    global delay
    global isSputtering
    global isRFOn
    global timer
    
    ser=serial.Serial(findPort(PSUPort), 38400, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  stopbits=1, rtscts=0, xonxoff=0)
    ArduinoUnoSerial = serial.Serial(findPort(ArduinoPort), 9600) 
    isRunning=True
    delay=0.5 #donotchange
    HEIGHT=400
    WIDTH=800
    isRFOn=False
    isSputtering=False
    forwardPower=0
    reversePower=0
    loadPower=0
    donePercent=0
    timer=0
    sputter = threading.Thread(target=sputterThread)
    sputter.start()

    while isRunning==True:
        pingOnce()
        print("ping")
        sleep(0.7)
        if isRFOn==True:
            forwardPower, reversePower, loadPower=GetPower()
            if isSputtering:
                print('Current Time Sputtered: ' + str(timer) + " ," + str(donePercent) + "%")
                if loadPower==0:
                    DeactivateRF()
                    print("PSU Shorted, please wait for timer to finish before continuing")
                    print("Time Sputtered: " + str(timer) + "\n" + "Percent Sputtered: " + str(donePercent))
            with open('power.csv', 'w', newline='') as f:
                thewriter=csv.writer(f)
                forwardPower, reversePower, loadPower=GetPower()
                thewriter.writerow([forwardPower, reversePower, loadPower])

    ArduinoUnoSerial.close()
    ser.close()

main()