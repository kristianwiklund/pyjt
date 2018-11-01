from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout,QPushButton
from PyQt5 import QtNetwork
import wsjtxudp

class Gui():
    maxx=5 # no more than this number of callsigns on the same line
    cx=0
    cy=0

    app = QApplication([])
    window = QWidget()
    layout = QGridLayout()
    
    def __init__(self):
    
        self.window.setLayout(self.layout)
        self.window.show()

    def buttonclick(self, who, ident, tid, snr, dtime, dfreq, mode, msg, conf, mods, theudpport):
        #print ("Responding to "+who)
        a = wsjtxudp.encode_reply(who, ident, tid, snr, dtime, dfreq, mode, msg, conf, mods)
        print(who)
        print(ident)
        print(tid) # ms since midnight
        print(snr)
        print (dtime)
        print(dfreq)
        print(mode)
        print(msg)
        print(conf)
        print(mods)
        
        s = QtNetwork.QUdpSocket()
        s.writeDatagram(a, QtNetwork.QHostAddress.LocalHost, theudpport)

        
    def start(self):
        self.app.exec_()

    def cleanup(self):

        for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
                
        #print ("deleted buttons")
        self.cx = 0
        self.cy = 0
        # remove all old buttons
        return
        #print("banana")
    
    def addcq(self,msg):
        # add new button
        # disbled for now
        if msg["call"] == "CQ":
        #    print (msg)
            return
        
        #print (str(msg["time"])+" CQ "+msg["call"])

        w = QPushButton(msg["call"])
        #def buttonclick(self, who, ident, tid, snr, dtime, dfreq, mode, msg, conf, mods):
        w.clicked.connect(lambda:self.buttonclick(msg["call"],
                                                  msg["id"],
                                                  msg["time"],
                                                  msg["snr"],
                                                  msg["dtime"],
                                                  msg["dfreq"],
                                                  msg["mode"],
                                                  msg["messageraw"],
                                                  msg["conf"],
                                                  0,
                                                  msg["udpport"]))
        self.layout.addWidget(w, self.cy, self.cx)
        print (msg["message"]+" " +msg["mode"].decode("utf-8"))
        #print(str(self.cx)+" "+str(self.cy))
        self.cx = self.cx + 1
        if self.cx>self.maxx:
            self.cx=0
            self.cy = self.cy + 1
