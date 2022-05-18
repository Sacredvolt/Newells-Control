import serial
from time import sleep

from PSU import GetControl, RelControl, autoSetTunerCaps

PSUPort="USB Serial Port"
ArduinoPort="Arduino Uno"
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
                

