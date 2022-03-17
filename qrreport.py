import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QProgressBar
import time
import requests
import qrcode
import webbrowser

class Qrreport(QDialog):
    def __init__(self, id_val):
        super().__init__()
        self.id_val = id_val
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle('링커버스 닥터 분석')
        #self.setGeometry(100, 100, 200, 100)
        self.resize(800, 480)
        layout = QVBoxLayout()
        #layout.addStretch(1)
        #self.addr = "https://innail.linkerverse.net/report/"+self.id_val+"/"
        self.addr = "http://192.168.17.20:8000/report/"+self.id_val+"/"
        img = qrcode.make(self.addr)
        img.save("gotoinnail.jpg")
        pixmap = QPixmap("gotoinnail.jpg")
        self.qr_img = QLabel()
        #self.qr_img.setGeometry(200, 0, 400, 400)
        #self.qr_img.setFixedSize(400,400)
        self.qr_img.setPixmap(pixmap)
        layout_h = QHBoxLayout()
        layout_h.addWidget(self.qr_img)
        
        
        font_notice= QtGui.QFont()
        font_notice.setPointSize(26)
        font_notice.setBold(True)
        
        self.button_url = QPushButton()
        self.button_url.setText("바로가기")
        self.button_url.setFont(font_notice)
        self.button_url.clicked.connect(lambda: webbrowser.open(self.addr))
        layout_h.addWidget(self.button_url)
        layout.addLayout(layout_h)
       
     
        layout.addStretch(1)
        self.setLayout(layout)
        
         #쓰레드 인스턴스 생성
         
         
       

    def showModal(self):

        return super().exec_()