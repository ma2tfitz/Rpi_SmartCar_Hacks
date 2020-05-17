#!/usr/bin/env python
import sys
import socketserver

command_descriptions = [
    "DRIVE_LEFT",
    "DRIVE_UP",
    "DRIVE_RIGHT",
    "DRIVE_DOWN",
    "DRIVE_LEFT_STOP",
    "DRIVE_STOP",
    "DRIVE_RIGHT_STOP",
    "CAMERA_RIGHT",
    "CAMERA_LEFT",
    "CAMERA_UP",
    "CAMERA_DOWN",
    "START_TRACK",
    "12",
    "13",
    "14",
    "BEEP_ON",
    "BEEP_OFF",
    "START_AVOID",
    "18",
    "SHUTDOWN",
    ]


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        client, port = self.client_address

        print("Connection from", client, port)
        self.request.sendall(b'{"version":2}') # handshake; tells app what protocol to use

        while True:
            buf = self.request.recv(8192)
            if len(buf) > 0:
                out = []
                for x in buf:
                    out.append("{:02d}".format(x))
                    out.append(" ")
                    if x >= 32 and x <= 126:
                        out.append(chr(x))
                    else:
                        out.append(".")
                    out.append(" ")
                    if x < len(command_descriptions):
                        out.append(command_descriptions[x])
                    else:
                        out.append("")
                    out.append(" ")
                print("".join(out))
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        #self.request.sendall(b"return value2")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    HOST, PORT = "0.0.0.0", 2001

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
