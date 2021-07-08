import time
import bluetooth

import threading
import socket
import sys

from mindwavemobile.MindwaveDataPoints import *
from mindwavemobile.MindwaveDataPointReader import *
import textwrap

def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break
#print ('\r\n\r\nTello Python3 Demo.\r\n')
#print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')
#print ('end -- quit demo.\r\n')

def drone(command, tello):
    try:
        msg = command;
        #print (msg)
        """if not msg:
            break  """
        if 'end' in msg:
            print ('...')
            sock.close()
        # Send data
        msg = msg.encode(encoding="utf-8")
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()

if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    if (mindwaveDataPointReader.isConnected()):

        host = ''
        port = 9000
        locaddr = (host,port)
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tello_address = ('192.168.10.1', 8889)
        sock.bind(locaddr)
        recvThread = threading.Thread(target=recv)
        recvThread.start()
        drone("command", tello_address)
        print("Drone Start")
        while(True):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            dataW = dataPoint.__class__
            if (dataW is AttentionDataPoint):
                atte = int(dataPoint.attentionValue)
                print(dataPoint)
                if (atte <= 10 and atte > 5 and atte < 30):
                    print("Taking Off")
                    drone("takeoff", tello_address)
                    time.sleep(2)
                elif (atte >= 30 and atte < 60):
                    print("Forward")
                    drone("takeoff", tello_address)
                    time.sleep(.5)
                    drone("forward 20", tello_address)
                    time.sleep(2)
                elif (atte >= 60 and atte < 65):
                    print("Flip")
                    drone("takeoff", tello_address)
                    time.sleep(.5)
                    drone("flip r", tello_address)
                    time.sleep(2)
                elif (atte >= 65 and atte < 70):
                    print("Flip")
                    drone("takeoff", tello_address)
                    time.sleep(.5)
                    drone("flip l", tello_address)
                    time.sleep(2)
                elif (atte >= 70 and atte < 80):
                    print("Flip")
                    drone("takeoff", tello_address)
                    time.sleep(.5)
                    drone("flip b", tello_address)
                    time.sleep(2)
                elif (atte >= 80):
                    print("Rotating")
                    drone("takeoff", tello_address)
                    time.sleep(.5)
                    drone("cw 3600", tello_address)
                    time.sleep(2)
                elif (atte <= 5 and atte > 0):
                    print("Goodbye")
                    drone("land", tello_address)
                    time.sleep(2)
                elif (atte == 0):
                    print("Goodbye")
                    drone("land", tello_address)

    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " ")))
