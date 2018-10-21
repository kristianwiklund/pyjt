# initial version: decodes decode udp messages and prints CQ messages

import pyhamtools
import socket
import wsjtxudp
import socketserver
#import gui

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        msg = wsjtxudp.decode(data) # this contains a dictionary with decoded data        
        

UDP_IP = "127.0.0.1"
UDP_PORT = 2237

server= socketserver.UDPServer((UDP_IP, UDP_PORT), MyUDPHandler)
if server:
    server.serve_forever()


gui.setup()



    

    
