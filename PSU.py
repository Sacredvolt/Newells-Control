
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
    print(command.hex())
    reply=SendCommand(command)
    return reply
        
def ActivateRF():
    global isRFOn
    reply=GenAndSend('4252','5555','0000')
    print(reply.hex())
    isRFOn=True
    return reply

def DeactivateRF():
    global isRFOn
    reply=GenAndSend('4252','0000','0000')
    print(reply.hex())
    isRFOn=False
    return reply
#########################################################
        
def openValvesfor(gun, s_timer):
    global isRunning
    global isSputtering
    print ("You will sputter Gun " + str(gun) +"for" +str(s_timer) +"seconds" )
    GunSelect(gun)
    if gun==1:
        ValRelease1(delay)
        ShutterOpen1(delay)
        sleep(s_timer-4)
        ShutterClose1(delay)
        ValRelease1(delay)
        print ("sputtering done on gun 1")
    elif gun==2:
        ValRelease2(delay)
        ShutterOpen2(delay)
        sleep(s_timer-4)
        ShutterClose2(delay)
        ValRelease2(delay)
        print ("sputtering done on gun 2")
    sleep(delay)
    DeactivateRF()
    isSputtering=False
    sleep(delay)
    SetPower(0)