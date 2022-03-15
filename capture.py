# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capture.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
# from AdapterBoard import MultiAdapter
from PyQt5.QtCore import *
from PyQt5 import QtGui

class testThread(QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = False

 
    def run(self):
        while self.isRun:
            print('쓰레드 : ' + str(self.n))
 
            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
            self.threadEvent.emit(self.n)
            self.n += 1
            time.sleep(0.3)

class Capture(QDialog):
    adapter = 0
    skipFrame = 12
    counter = 20
    imageFiles = []
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('손톱 촬영')
        #self.setGeometry(10, 10, 790, 440)
        layout_0 = QHBoxLayout()
        layout_l = QVBoxLayout()
        #layout.addStretch(1)
        #Preview
        pixmap = QPixmap("faust_github.jpg")
        self.lbl_img = QLabel()
        #self.lbl_img.resize(600, 340)
        #pixmap=pixmap.scaledToHeight(340)
        self.lbl_img.setFixedSize(520,370)
        self.lbl_img.setPixmap(pixmap)
 
        #Retry , upload
        subLayout_l = QHBoxLayout()
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)

        self.btnOK = QPushButton("분석하기")
        self.btnOK.clicked.connect(self.onOKButtonClicked)
        self.btnOK.setFont(font)

        self.btnCancel = QPushButton("다시촬영")
        self.btnCancel.clicked.connect(self.onCancelButtonClicked)
        self.btnCancel.setFont(font)
        #layout.addWidget(edit)
        layout_l.addWidget(self.lbl_img)
        
        subLayout_l.addWidget(self.btnOK)
        subLayout_l.addWidget(self.btnCancel)
        layout_l.addLayout(subLayout_l)
        layout_0.addLayout(layout_l,3)


        imgfont = QtGui.QFont()
        imgfont.setPointSize(52)

        labelfont = QtGui.QFont()
        labelfont.setPointSize(16)
        

        layout_r = QVBoxLayout()
        #layout_r.resize(170, 460)
        self.label_A = QLabel("사진 1")
        self.label_A.setFont(labelfont)
        #self.label_A.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label_A.resize(161, 24)
        self.label_A.setObjectName("cam_A")

        self.label_A_thumeb = QLabel("")
        #self.label_A_thumeb.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label_A_thumeb.setFixedSize(144,100)
        self.label_A_thumeb.setObjectName("cam_A_thumb")
        self.label_A_thumeb.setStyleSheet("color: #FF5733; border-style: solid; border-width: 2px; border-color: #FFC300; border-radius: 10px; ")
        self.label_A_thumeb.setFont(imgfont)

        self.label_B = QLabel("사진 2")
        #self.label_A.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label_B.resize(161, 24)
        self.label_B.setFont(labelfont)
        self.label_B.setObjectName("cam_B")

        self.label_B_thumeb = QLabel()
        #self.label_A_thumeb.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label_B_thumeb.setFixedSize(144,100)
        self.label_B_thumeb.setObjectName("cam_B_thumb")
        self.label_B_thumeb.setStyleSheet(
            "color: #4D69E8; border-style: solid; border-width: 2px; border-color: #54A0FF; border-radius: 10px; ")
        self.label_B_thumeb.setFont(imgfont)

        self.label_C = QLabel("사진 3")
        #self.label_A.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label_C.resize(161, 24)
        self.label_C.setFont(labelfont)
        self.label_C.setObjectName("cam_C")

        self.label_C_thumeb = QLabel()
        #self.label_A_thumeb.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label_C_thumeb.setFixedSize(144,100)
        self.label_C_thumeb.setObjectName("cam_C_thumb")
        self.label_C_thumeb.setStyleSheet(
            "color: #41E881; border-style: solid; border-width: 2px; border-color: #67E841; border-radius: 10px; ")
        self.label_C_thumeb.setFont(imgfont)

        layout_r.addWidget(self.label_A)
        layout_r.addWidget(self.label_A_thumeb)
        layout_r.addWidget(self.label_B)
        layout_r.addWidget(self.label_B_thumeb)
        layout_r.addWidget(self.label_C)
        layout_r.addWidget(self.label_C_thumeb)


        layout_0.addLayout(layout_r,1)
        #layout.addStretch(1)
        self.setLayout(layout_0)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        #쓰레드 인스턴스 생성
        self.th = testThread(self)

        #쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.threadEventHandler)

        print('threadEventHandler : 쓰레드 시작')
        self.th.isRun = True
        self.th.start()
        self.counter = self.skipFrame
        self.imageFiles.clear()

    def onOKButtonClicked(self):
        if self.th.isRun:
            print('threadEventHandler : 쓰레드 정지')
            self.th.exit()
            self.th.isRun = False

        #self.accept()

    def onCancelButtonClicked(self):
        if not self.th.isRun:
            print('threadEventHandler : 쓰레드 시작')
            self.th.isRun = True
            self.th.start()
            self.counter = self.skipFrame
            self.imageFiles.clear()
            if self.adapter.camOk == True:
                self.adapter.select_channel(chr(65+self.adapter.cam_i))
                print("카메라선택 -" + chr(65+self.adapter.cam_i))


        #self.reject()

    def threadEventHandler(self, n):
        print("threadEventHandler")
        if self.th.n ==10:
            self.th.exit()
            self.th.isRun = False
            #self.close()
            self.accept()
            
        # if self.adapter.camOk == True:
        #     print('self.adapter.camOk == True')
        #     self.counter = self.counter -1
        #     if self.counter ==0:
        #         self.counter = self.skipFrame
        #         self.adapter.saveCapture()
        #         self.imageFiles.append(self.adapter.jpgname)
        #         capture = QPixmap(self.adapter.jpgname)
        #         cpture=cacapture.scaledToHeight(120)
        #         if self.adapter.cam_i == 0:
        #             self.label_A_thumeb.setPixmap(capture)
        #         elif self.adapter.cam_i == 1:
        #             self.label_B_thumeb.setPixmap(capture)
        #         else:
        #             self.label_C_thumeb.setPixmap(capture)

        #         self.adapter.cam_i = self.adapter.cam_i +1
        #         if self.adapter.cam_i == 3:
        #             print('threadEventHandler : 쓰레드 정지')
        #             self.th.exit()
        #             self.th.isRun = False
        #             self.adapter.cam_i = 0
        #             return
        #         self.adapter.select_channel(chr(65+self.adapter.cam_i))
        #         print("카메라변경 -" + chr(65+self.adapter.cam_i))

        #     else:
        #         self.adapter.preview2()
        #         self.lbl_img.setPixmap(self.adapter.pixmap)
        # else:
        #     self.adapter.select_channel('A')
        #     print("카메라선택 - A")


    def showModal(self):
        # self.adapter = _adapter
        #self.showMaximized()
        return super().exec_()

    def closeEvent(self, event):
        if self.th.isRun:
            print('메인 : 쓰레드 정지')
            self.th.exit()
            self.th.isRun = False