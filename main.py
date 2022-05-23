#########################################################  
import serial
from time import sleep
import threading
import tkinter as tk
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
    reply = setTunerManual()
    sleep(0.1)
    reply = setLoadTunerCapPosition()
    sleep(0.5)
    reply = setTuneTunerCapPosition()
    sleep(0.5)
    reply = setTunerAuto()
    sleep(0.1)
    return reply

def ActivateRF():
    global isRFOn
    autoSetTunerCaps()
    reply=GenAndSend('4252','5555','0000')
    isRFOn=True
    return reply

def DeactivateRF():
    global isRFOn
    global isSputtering
    global timer
    global donePercent
    reply=GenAndSend('4252','0000','0000')
    isRFOn=False
    isSputtering=False
    timer=0
    donePercent=0
    return reply

###############################################################################################################

PSUPort="USB Serial Port"
ArduinoPort="Arduino Uno"
PSUPID="USB VID:PID=0403:6001"
ArduinoPID="USB VID:PID=2341:004"

def findPort(portName):
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        return None
    if comports:
        com_ports_list = comports()
        ports=[]
        for port, desc, hwid in sorted(com_ports_list):
            ports.append([port, desc, hwid])
        
        foundPort = None
        for port in ports:
            if port[2].startswith(portName):
                foundPort = port[0]  # Success; found by name match.
                break  # stop searching-- we are done.
        print(foundPort)
        return foundPort 
    
###############################################################################################################
                
def ValCloseAll1(delay):
    ArduinoUnoSerial.write('ac'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('cc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('dc'.encode())
    sleep(delay)
    return (0)

def ShutterOpen1(delay):
    ArduinoUnoSerial.write('ac'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bo'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('do'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('co'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('cc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('ao'.encode())
    sleep(delay)
    return(0)

def ShutterClose1(delay):
    ArduinoUnoSerial.write('ac'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bo'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('do'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('co'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('dc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('ao'.encode())
    sleep(delay)

def ValRelease1(delay):   
    ArduinoUnoSerial.write('ac'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bo'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('do'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('co'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('dc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('cc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('bc'.encode())

def ShutterOpen2(delay):
    ArduinoUnoSerial.write('ec'.encode()) #a=e, b=f, c=g, d=h
    sleep(delay)
    ArduinoUnoSerial.write('fo'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('ho'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('go'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('fc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('gc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('eo'.encode())
    sleep(delay)
    return(0)

def ShutterClose2(delay):
    ArduinoUnoSerial.write('ec'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('fo'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('ho'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('go'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('fc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('hc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('eo'.encode())
    sleep(delay)

def ValRelease2(delay):   
    ArduinoUnoSerial.write('ec'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('fo'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('ho'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('go'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('hc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('gc'.encode())
    sleep(delay)
    ArduinoUnoSerial.write('fc'.encode())
    
def GunSelect(num):
    print ("selecting gun "+str(num))
    if num==1:
        ArduinoUnoSerial.write('t'.encode())
        sleep(delay)
    if num==2:
        ArduinoUnoSerial.write('s'.encode())
        sleep(delay)
    # else:
    #     print ("Invalid Input, Enter 1 or 2")
    print ("RF switch set to gun " +str(num))
    
def openValvesfor(gun, s_timer):
    global isRunning
    global isSputtering
    global donePercent
    global timer
    
    print ("You will sputter Gun " + str(gun) +"for" +str(s_timer) +"seconds" )
    GunSelect(gun)
    isSputtering=True
    if gun==1:
        ValRelease1(delay)
        ShutterOpen1(delay)
        #sleep(s_timer-4)
        timer+=4
        while timer<s_timer:
            sleep(1)
            timer+=1
            donePercent=round((timer/(s_timer) * 100),2)
        ShutterClose1(delay)
        ValRelease1(delay)
        print ("sputtering done on gun 1")
    elif gun==2:
        ValRelease2(delay)
        ShutterOpen2(delay)
        #sleep(s_timer-4)
        timer+=4
        while timer<s_timer:
            sleep(1)
            timer+=1
            donePercent=round((timer/(s_timer-4) * 100),2)
        ShutterClose2(delay)
        ValRelease2(delay)
        print ("sputtering done on gun 2")
    sleep(delay)
    DeactivateRF()
    timer=0
    donePercent=0
    isSputtering=False
    sleep(delay)
    SetPower(0)

###############################################################################################################

def sputterThread():
    global isRunning
    global ser
    global delay
    global HEIGHT
    global WIDTH
    global isRFOn
    global donePercent
    global entry4
    
    while isRunning==True:
        root = tk.Tk()
        canvas=tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        
        buttonFrame=tk.Frame(root, bg="black", bd=10)
        buttonFrame.place(relx = 0.01,rely=0.01, relwidth=0.98, relheight=0.98)        
        button1 = tk.Button(buttonFrame, text="Get Control", fg='white', bg='grey', command=lambda: GetControl())
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
                
        label5 = tk.Label(buttonFrame, text="Set Tuner Caps", fg='white', bg='black')
        label5.grid(row=5, column=0)
        button5=tk.Button(buttonFrame, text="Confirm", fg='white', bg='grey', command=lambda:autoSetTunerCaps())
        button5.grid(row=5, column=1, rowspan=1)
        
        # label6 = tk.Label(buttonFrame, text="Set Tuner Caps", fg='white', bg='black')
        # label6.grid(row=6, column=0)
        # button6=tk.Button(buttonFrame, text="Manual", fg='white', bg='grey', command=lambda:setTunerManual())
        # button6.grid(row=6, column=1, rowspan=1)
        # button62=tk.Button(buttonFrame, text="Auto", fg='white', bg='grey', command=lambda:setTunerAuto())
        # button62.grid(row=6, column=2, rowspan=1)
        
        root.mainloop()
        isRunning=False
    return

ser=serial.Serial(findPort(PSUPID), 38400, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  stopbits=1, rtscts=0, xonxoff=0)
ArduinoUnoSerial = serial.Serial(findPort(ArduinoPID), 9600) 
isRunning=True
delay=0.5 #donotchange
sleep(delay)
HEIGHT=600
WIDTH=600
isRFOn=False
isSputtering=False
forwardPower=0
reversePower=0
loadPower=0
donePercent=0
timer=0

sputter = threading.Thread(target=sputterThread)
sputter.start()
sleep(0.7)
GetControl()

while isRunning==True:
    sleep(0.7)
    if isRFOn==True:
        forwardPower, reversePower, loadPower=GetPower()
        if isSputtering:
            print('Current Time Sputtered: ' + str(timer) + " ," + str(donePercent) + "%")
            if loadPower==0:
                DeactivateRF()
                s_timer=int(entry4.get())
                timer=s_timer+1
                print("PSU Shorted, please wait for valves to close before continuing")
                print("Time Sputtered: " + str(timer) + "\n" + "Percent Sputtered: " + str(donePercent))
    else:
        pingOnce()
        print("ping")

ArduinoUnoSerial.close()
ser.close()
