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