#!/usr/bin/env python
import sys
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        client, port = self.client_address
        print("Connection from", client, port)

        # handshake; tells app what protocol to use
        self.request.sendall(b'{"version":2}')

        while True:
            buf = self.request.recv(8192)
            if buf:
                out = ["{:02d} ".format(x) for x in buf]
                print("".join(out))

if __name__ == "__main__":
    # HOST, PORT = "localhost", 8080
    HOST, PORT = "0.0.0.0", 2001

    # Create the server
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
