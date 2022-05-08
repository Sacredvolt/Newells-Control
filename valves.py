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
    timer=0
    print ("You will sputter Gun " + str(gun) +"for" +str(s_timer) +"seconds" )
    GunSelect(gun)
    if gun==1:
        ValRelease1(delay)
        ShutterOpen1(delay)
        #sleep(s_timer-4)
        while timer<s_timer-4:
            sleep(1)
            timer+=1
            donePercent=round((timer/(s_timer-4) * 100),2)
        ShutterClose1(delay)
        ValRelease1(delay)
        print ("sputtering done on gun 1")
    elif gun==2:
        ValRelease2(delay)
        ShutterOpen2(delay)
        #sleep(s_timer-4)
        while timer<s_timer-4:
            sleep(1)
            timer+=1
            donePercent=round((timer/(s_timer-4) * 100),2)
        ShutterClose2(delay)
        ValRelease2(delay)
        print ("sputtering done on gun 2")
    sleep(delay)
    DeactivateRF()
    isSputtering=False
    sleep(delay)
    SetPower(0)