from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout,QPushButton

app = QApplication([])
window = QWidget()
layout = QGridLayout()

def setup():
    layout.addWidget(QPushButton("A"),0,0)
    layout.addWidget(QPushButton("B"),0,1)
    layout.addWidget(QPushButton("C"),1,0)
    layout.addWidget(QPushButton("D"),1,1)
    window.setLayout(layout)
    window.show()
    app.exec_()
