# initial version: decodes decode udp messages and prints CQ messages

import pyhamtools
import socket
import wsjtxudp
import socketserver
import threading
from PyQt5 import QtNetwork
import gui

class myudp(QtNetwork.QUdpSocket):

    def __init__(self, parent=None):
        super(myudp, self).__init__(parent)
        self.socket = QtNetwork.QUdpSocket(self)
        self.socket.bind(2237)
        self.socket.readyRead.connect(self.handle)
    
    def handle(self):
        while self.socket.hasPendingDatagrams():
            data, host, port = self.socket.readDatagram(self.socket.pendingDatagramSize())
            msg = wsjtxudp.decode(data) # this contains a dictionary with decoded data        

udphandler = myudp()
gui.setup()



    

    
