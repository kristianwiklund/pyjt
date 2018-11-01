from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout,QPushButton


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

    def start(self):
        self.app.exec_()

    def cleanup(self):

        for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
                
        print ("deleted buttons")
        # remove all old buttons
        return
        #print("banana")
    
    def addcq(self,msg):
        # add new button
        # disbled for now
        if msg["call"] == "CQ":
            print (msg)
        print (str(msg["time"])+" CQ "+msg["call"])

    
        self.layout.addWidget(QPushButton(msg["call"]),self.cy,self.cx)
        self.cx = self.cx + 1
        if self.cx>self.maxx:
            self.cx=0
            self.cy = self.cy + 1
