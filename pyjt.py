# initial version: decodes decode udp messages and prints CQ messages

import wsjtxudp
import plistlib

from PyQt5 import QtNetwork
import gui

#mylol = pyhamtools.LookupLib(lookuptype="qrz")
#cic = pyhamtools.Callinfo(mylol)



class myudp(QtNetwork.QUdpSocket):

    lasttimestamp=0
    
    def __init__(self, mgui, parent=None):
        super(myudp, self).__init__(parent)
        self.socket = QtNetwork.QUdpSocket(self)
        self.socket.bind(2237)
        self.socket.readyRead.connect(self.handle)
        self.gui = mgui
        
    def handle(self):
        while self.socket.hasPendingDatagrams():
            data, host, port = self.socket.readDatagram(self.socket.pendingDatagramSize())
            msg = wsjtxudp.decode(data) # this contains a dictionary with decoded data        
            #           print (cic.get_all(msg["call"]))

            if msg["type"]==2 and msg["cq"]:
                if msg["dtime"]>self.lasttimestamp:
                    self.lasttimestamp = msg["dtime"]
                    self.gui.cleanup()

                self.gui.addcq(msg)
                
mgui = gui.Gui()                
udphandler = myudp(mgui)
mgui.start()



    

    
