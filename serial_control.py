import serial
from time import sleep

PSUPort="USB Serial Port"
WinPSUComport1="COM6"
WinPSUComport2="COM5"
LinuxPSUComport1="/dev/ttyUSB0"
LinuxPSUComport2="/dev/ttyUSB1"

def findPort(portName):
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        return None
    if comports:
        com_ports_list = list(comports())
        foundPort = None
        for port in com_ports_list:
            if port[1].startswith(portName):
                foundPort = port[0]  # Success; found by name match.
                break  # stop searching-- we are done.
        return foundPort 
    
def tryToOpenPSUPort(): 
    try:
        ser = serial.Serial(LinuxPSUComport1, 38400, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  stopbits=1, rtscts=0, xonxoff=0)
        print('connected')
    except serial.SerialException:
        try:
            ser = serial.Serial(LinuxPSUComport2, 38400, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  stopbits=1, rtscts=0, xonxoff=0)
            print('connected')
        except serial.SerialException:
            try:
                ser = serial.Serial(WinPSUComport1, 38400, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  stopbits=1, rtscts=0, xonxoff=0)
                print('connected')
            except serial.SerialException:
                try:
                    ser = serial.Serial(WinPSUComport2, 38400, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  stopbits=1, rtscts=0, xonxoff=0)
                    print('connected')
                except serial.SerialException:
                    print('can not find port, aborting')
                    return None