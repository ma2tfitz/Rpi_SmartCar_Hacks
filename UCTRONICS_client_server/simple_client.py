#!/usr/bin/env python
import socket
import sys
import time

#HOST, PORT = "localhost", 2001
#HOST, PORT = "192.168.8.10", 2001 # station mode
HOST, PORT = "192.168.1.1", 2001 # ap mode

DRIVE_LEFT = bytes((0,))
DRIVE_UP = bytes((1,))
DRIVE_RIGHT = bytes((2,))
DRIVE_DOWN = bytes((3,))
DRIVE_STOP = bytes((5,))

DRIVE_LEFT_STOP = bytes((4,))
DRIVE_RIGHT_STOP = bytes((6,))

CAMERA_RIGHT = bytes((7,))
CAMERA_LEFT = bytes((8,))
CAMERA_UP = bytes((9,))
CAMERA_DOWN = bytes((10,))

BEEP_ON = bytes((15,))
BEEP_OFF = bytes((16,))

START_TRACK = bytes((11,))
START_AVOID = bytes((17,))
SHUTDOWN = bytes((19,))

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(BEEP_ON)
    time.sleep(0.1)
    sock.sendall(BEEP_OFF)

    for i in range(8):
        sock.sendall(DRIVE_UP)
        time.sleep(0.5)
        sock.sendall(DRIVE_STOP)

        sock.sendall(DRIVE_LEFT)
        time.sleep(.31)
        sock.sendall(DRIVE_LEFT_STOP)
        sock.sendall(DRIVE_STOP)

    for i in range(3):
        sock.sendall(BEEP_ON)
        time.sleep(0.1)
        sock.sendall(BEEP_OFF)
        time.sleep(0.1)

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
    print("received", received)
