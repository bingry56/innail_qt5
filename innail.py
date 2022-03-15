# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'innail.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#import AdapterBoard 
import time
import os
import cv2 as cv 
import numpy as np  
#import RPi.GPIO as GPIO
#import board
#import adafruit_mlx90614

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from capture import Capture
from uploading import Uploading
from qrreport import Qrreport
from functools import partial
import errno

#Arducam_adapter_board = AdapterBoard.MultiAdapter()
editFocusIndex =0

user_sex = 0
user_age = 0
user_height = 0
user_weight = 0
num_h = 90
num_w = 80



class testThread(QtCore.QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(int)
 
    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = False
 
    def run(self):

        while self.isRun:
            #print('쓰레드 : ' + str(self.n))
            # if Arducam_adapter_board.camOk == False:
            #     Arducam_adapter_board.init()
            #     Arducam_adapter_board.select_channel('A')
            
            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
            self.threadEvent.emit(self.n)
            
            self.n += 1
            time.sleep(0.8)

class UserInfoEdit(QtWidgets.QTextEdit):
    index = 0
    def focusInEvent(self, e):
        global editFocusIndex
        editFocusIndex = self.index
        print("index :" +str(self.index))
        # Do something with the event here
        super(UserInfoEdit, self).focusInEvent(e) # Do the default action on the parent class QLineEdit   
    
class Ui_MainWindow(object):
    showMessageBox = QtCore.pyqtSignal(str, str, str, str)
    hand_on =0
    hand_off = 0
    cnt = 0
    def on_show_message_box(self, id, severity, title, text):
        self.responses[str(id)] = getattr(QtGui.QMessageBox, str(severity))(self, title, text)

    def setupUi(self, MainWindow):

        #Arducam_adapter_board.init()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(0, 0, 800, 460)
        #MainWindow.resize(800, 480)
        MainWindow.setWindowOpacity(2.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        digitfont = QtGui.QFont()
        digitfont.setPointSize(48)
        digitfont.setBold(True)
        #digitfont.setItalic(True)
        digitfont.setWeight(75)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        self.num_1 = QtWidgets.QPushButton(self.centralwidget)
        self.num_1.setGeometry(QtCore.QRect(460, 20, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_1.sizePolicy().hasHeightForWidth())
        self.num_1.setSizePolicy(sizePolicy)
        self.num_1.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_1.setBaseSize(QtCore.QSize(70, 80))
        self.num_1.setFont(digitfont)
        self.num_1.setAutoFillBackground(False)
        self.num_1.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_1.setAutoDefault(False)
        self.num_1.setDefault(False)
        self.num_1.setObjectName("num_1")
        self.num_1.clicked.connect(lambda:self.onNumButtonClicked(1))

        self.num_2 = QtWidgets.QPushButton(self.centralwidget)
        self.num_2.setGeometry(QtCore.QRect(560, 20, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_2.sizePolicy().hasHeightForWidth())
        self.num_2.setSizePolicy(sizePolicy)
        self.num_2.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_2.setBaseSize(QtCore.QSize(70, 80))
        self.num_2.setFont(digitfont)
        self.num_2.setAutoFillBackground(False)
        self.num_2.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_2.setAutoDefault(False)
        self.num_2.setDefault(False)
        self.num_2.setObjectName("num_2")
        self.num_2.clicked.connect(lambda:self.onNumButtonClicked(2))

        self.num_3 = QtWidgets.QPushButton(self.centralwidget)
        self.num_3.setGeometry(QtCore.QRect(660, 20, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_3.sizePolicy().hasHeightForWidth())
        self.num_3.setSizePolicy(sizePolicy)
        self.num_3.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_3.setBaseSize(QtCore.QSize(70, 80))
        self.num_3.setFont(digitfont)
        self.num_3.setAutoFillBackground(False)
        self.num_3.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_3.setAutoDefault(False)
        self.num_3.setDefault(False)
        self.num_3.setObjectName("num_3")
        self.num_3.clicked.connect(lambda:self.onNumButtonClicked(3))

        self.num_4 = QtWidgets.QPushButton(self.centralwidget)
        self.num_4.setGeometry(QtCore.QRect(460, 120, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_4.sizePolicy().hasHeightForWidth())
        self.num_4.setSizePolicy(sizePolicy)
        self.num_4.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_4.setBaseSize(QtCore.QSize(70, 80))
        self.num_4.setFont(digitfont)
        self.num_4.setAutoFillBackground(False)
        self.num_4.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_4.setAutoDefault(False)
        self.num_4.setDefault(False)
        self.num_4.setObjectName("num_4")
        self.num_4.clicked.connect(lambda:self.onNumButtonClicked(4))

        self.num_5 = QtWidgets.QPushButton(self.centralwidget)
        self.num_5.setGeometry(QtCore.QRect(560, 120, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_5.sizePolicy().hasHeightForWidth())
        self.num_5.setSizePolicy(sizePolicy)
        self.num_5.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_5.setBaseSize(QtCore.QSize(70, 80))
        self.num_5.setFont(digitfont)
        self.num_5.setAutoFillBackground(False)
        self.num_5.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_5.setAutoDefault(False)
        self.num_5.setDefault(False)
        self.num_5.setObjectName("num_5")
        self.num_5.clicked.connect(lambda:self.onNumButtonClicked(5))

        self.num_6 = QtWidgets.QPushButton(self.centralwidget)
        self.num_6.setGeometry(QtCore.QRect(660, 120, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_6.sizePolicy().hasHeightForWidth())
        self.num_6.setSizePolicy(sizePolicy)
        self.num_6.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_6.setBaseSize(QtCore.QSize(70, 80))
        self.num_6.setFont(digitfont)
        self.num_6.setAutoFillBackground(False)
        self.num_6.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_6.setAutoDefault(False)
        self.num_6.setDefault(False)
        self.num_6.setObjectName("num_6")
        self.num_6.clicked.connect(lambda:self.onNumButtonClicked(6))

        self.num_7 = QtWidgets.QPushButton(self.centralwidget)
        self.num_7.setGeometry(QtCore.QRect(460, 220, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_7.sizePolicy().hasHeightForWidth())
        self.num_7.setSizePolicy(sizePolicy)
        self.num_7.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_7.setBaseSize(QtCore.QSize(70, 80))
        self.num_7.setFont(digitfont)
        self.num_7.setAutoFillBackground(False)
        self.num_7.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_7.setAutoDefault(False)
        self.num_7.setDefault(False)
        self.num_7.setObjectName("num_7")
        self.num_7.clicked.connect(lambda:self.onNumButtonClicked(7))
        
        self.num_8 = QtWidgets.QPushButton(self.centralwidget)
        self.num_8.setGeometry(QtCore.QRect(560, 220, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_8.sizePolicy().hasHeightForWidth())
        self.num_8.setSizePolicy(sizePolicy)
        self.num_8.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_8.setBaseSize(QtCore.QSize(70, 80))
        self.num_8.setFont(digitfont)
        self.num_8.setAutoFillBackground(False)
        self.num_8.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_8.setAutoDefault(False)
        self.num_8.setDefault(False)
        self.num_8.setObjectName("num_8")
        self.num_8.clicked.connect(lambda:self.onNumButtonClicked(8))

        self.num_9 = QtWidgets.QPushButton(self.centralwidget)
        self.num_9.setGeometry(QtCore.QRect(660, 220, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_9.sizePolicy().hasHeightForWidth())
        self.num_9.setSizePolicy(sizePolicy)
        self.num_9.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_9.setBaseSize(QtCore.QSize(70, 80))
        self.num_9.setFont(digitfont)
        self.num_9.setAutoFillBackground(False)
        self.num_9.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_9.setAutoDefault(False)
        self.num_9.setDefault(False)
        self.num_9.setObjectName("num_9")
        self.num_9.clicked.connect(lambda:self.onNumButtonClicked(9))

        self.num_0 = QtWidgets.QPushButton(self.centralwidget)
        self.num_0.setGeometry(QtCore.QRect(560, 320, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_0.sizePolicy().hasHeightForWidth())
        self.num_0.setSizePolicy(sizePolicy)
        self.num_0.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_0.setBaseSize(QtCore.QSize(70, 80))
        self.num_0.setFont(digitfont)
        self.num_0.setAutoFillBackground(False)
        self.num_0.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_0.setAutoDefault(False)
        self.num_0.setDefault(False)
        self.num_0.setObjectName("num_0")
        self.num_0.clicked.connect(lambda:self.onNumButtonClicked(0))

        self.num_11 = QtWidgets.QPushButton(self.centralwidget)
        self.num_11.setGeometry(QtCore.QRect(660, 320, num_w, num_h))
        sizePolicy.setHeightForWidth(self.num_11.sizePolicy().hasHeightForWidth())
        self.num_11.setSizePolicy(sizePolicy)
        self.num_11.setSizeIncrement(QtCore.QSize(70, 80))
        self.num_11.setBaseSize(QtCore.QSize(70, 80))
        self.num_11.setFont(digitfont)
        self.num_11.setAutoFillBackground(False)
        self.num_11.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.num_11.setAutoDefault(False)
        self.num_11.setDefault(False)
        self.num_11.setObjectName("back")
        self.num_11.clicked.connect(lambda:self.onNumButtonClicked(-1))

        font_label = QtGui.QFont()
        font_label.setPointSize(24)
        font_label.setBold(True)

        self.r_female = QtWidgets.QRadioButton(self.centralwidget)
        self.r_female.setGeometry(QtCore.QRect(50, 10, 171, 71)) 
        self.r_female.setFont(font_label)
        self.r_female.setObjectName("r_female")

        self.r_male = QtWidgets.QRadioButton(self.centralwidget)
        self.r_male.setGeometry(QtCore.QRect(240, 10, 141, 71))
        self.r_male.setFont(font_label)
        self.r_male.setChecked(True)
        self.r_male.setObjectName("r_male")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 90, 81, 61))

        self.label.setFont(font_label)
        self.label.setObjectName("label")


        font_edit= QtGui.QFont()
        font_edit.setPointSize(24)
        font_edit.setBold(True)

        self.textEdit = UserInfoEdit(self.centralwidget)
        self.textEdit.index = 0
        self.textEdit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit.setAlignment(QtCore.Qt.AlignRight)
        self.textEdit.setFont(font_edit)
        self.textEdit.setGeometry(QtCore.QRect(160, 90, 121, 56))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = UserInfoEdit(self.centralwidget)
        self.textEdit_2.index = 1
        self.textEdit_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_2.setAlignment(QtCore.Qt.AlignRight)
        self.textEdit_2.setFont(font_edit)
        self.textEdit_2.setGeometry(QtCore.QRect(160, 160, 121, 56))
        self.textEdit_2.setObjectName("textEdit_2")
 
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 160, 81, 61))

        self.label_2.setFont(font_label)
        self.label_2.setObjectName("label_2")
        self.textEdit_3 = UserInfoEdit(self.centralwidget)
        self.textEdit_3.index = 2
        self.textEdit_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_3.setAlignment(QtCore.Qt.AlignRight)
        self.textEdit_3.setFont(font_edit)
        self.textEdit_3.setGeometry(QtCore.QRect(160, 230, 121, 56))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 230, 81, 61))

        self.label_3.setFont(font_label)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(290, 90, 41, 61))

        self.label_4.setFont(font_label)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(290, 160, 51, 61))

        self.label_5.setFont(font_label)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(290, 230, 41, 61))

        self.label_6.setFont(font_label)
        self.label_6.setObjectName("label_6")
        self.capture_button = QtWidgets.QPushButton(self.centralwidget)
        self.capture_button.setGeometry(QtCore.QRect(60, 310, 271, 111))

        font = QtGui.QFont()
        font.setPointSize(38)
        font.setBold(True)
        self.capture_button.setFont(font)
        self.capture_button.setObjectName("capture_button")
        self.capture_button.clicked.connect(self.onButtonClicked)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #쓰레드 인스턴스 생성
        self.th = testThread(MainWindow)

        #쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.threadEventHandler)

        #BCM
        #GPIO.setmode(GPIO.BCM)
        self.pirPin = 16

        #Board
        #self.pirPin = 36

        # GPIO.setup(self.pirPin, GPIO.IN, GPIO.PUD_UP)

        # # The MLX90614 only works at the default I2C bus speed of 100kHz.
        # # A higher speed, such as 400kHz, will not work.
        # self.i2c = board.I2C()
        # self.mlx = adafruit_mlx90614.MLX90614(self.i2c)
                
        print('메인 : 쓰레드 시작')
        self.th.isRun = True
        self.th.start()

        try:
            if not(os.path.isdir("data")):
                os.makedirs(os.path.join("data"))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "링커버스 인네일 Doctor"))
        self.num_1.setText(_translate("MainWindow", "1"))
        self.num_2.setText(_translate("MainWindow", "2"))
        self.num_3.setText(_translate("MainWindow", "3"))
        self.num_4.setText(_translate("MainWindow", "4"))
        self.num_5.setText(_translate("MainWindow", "5"))
        self.num_6.setText(_translate("MainWindow", "6"))
        self.num_7.setText(_translate("MainWindow", "7"))
        self.num_8.setText(_translate("MainWindow", "8"))
        self.num_9.setText(_translate("MainWindow", "9"))
        self.num_0.setText(_translate("MainWindow", "0"))
        self.num_11.setText(_translate("MainWindow", "<"))
        self.r_female.setText(_translate("MainWindow", " 여자"))
        self.r_male.setText(_translate("MainWindow", "남자"))
        self.label.setText(_translate("MainWindow", "나이"))
        self.label_2.setText(_translate("MainWindow", "키"))
        self.label_3.setText(_translate("MainWindow", "체중"))
        self.label_4.setText(_translate("MainWindow", "세"))
        self.label_5.setText(_translate("MainWindow", "cm"))
        self.label_6.setText(_translate("MainWindow", "Kg"))
        self.capture_button.setText(_translate("MainWindow", "체온"))
        self.textEdit.setAlignment(QtCore.Qt.AlignRight)

    def onButtonClicked(self):
        # if Arducam_adapter_board.camOk == False:
        #     time.sleep(1)
        # Arducam_adapter_board.select_channel('A')
        win = Capture()
        r = win.showModal()
        print("dialog reture: " + str(r))
        
        if r == 1:
            upload = Uploading()
            r2 = upload.showModal()
            print("delivered : ival " + upload.id_val)
            gotoinnal = Qrreport(upload.id_val)
            r3 = gotoinnal.showModal()
            if r2 ==1:
                print(upload.id_val)
            
        
        
    def onNumButtonClicked(self, num):
        global user_age, user_height, user_weight
        print('onNumButtonClicked - ' + str(num))
        if editFocusIndex ==0:
            val = user_age
        elif editFocusIndex == 1:
            val = user_height
        else :
            val = user_weight

        if num == -1:    
            val = int(val/10)
        else:
            val = val*10 + num

        if editFocusIndex ==0:
            user_age = val
            self.textEdit.setText(str(user_age))
            self.textEdit.setAlignment(QtCore.Qt.AlignRight)
        elif editFocusIndex == 1:
            user_height = val
            self.textEdit_2.setText(str(user_height))
            self.textEdit_2.setAlignment(QtCore.Qt.AlignRight)
        else :
            user_weight = val
            self.textEdit_3.setText(str(user_weight))
            self.textEdit_3.setAlignment(QtCore.Qt.AlignRight)


    def threadEventHandler(self, n):
        #print('메인 : threadEvent(self,' + str(n) + ')')
        # temperature results in celsius
        #self.mlx = adafruit_mlx90614.MLX90614(self.i2c)
        # print("Ambent Temp: ", self.mlx.ambient_temperature)
        # print("Object Temp: ", self.mlx.object_temperature)

        # floatTemp = float(self.mlx.object_temperature)
        floatTemp=0
        tempAdjust = float(round(floatTemp + 3.0,1))

        _translate = QtCore.QCoreApplication.translate
        self.capture_button.setText(_translate("MainWindow", str(tempAdjust)))

        self.cnt = self.cnt +1
        # if GPIO.input(self.pirPin) !=  GPIO.LOW:
        #     print ("Motion detected!" +str(self.cnt))
        #     self.hand_on = self.hand_on+1

        # else:
        #     print ("No motion"+str(self.cnt))
        #     self.hand_off = self.hand_off +1
        #     if self.hand_off > 6:
        #         self.hand_off = 0
        #         self.hand_on = 0
        if self.hand_on >6 :
            self.hand_off = 0
            self.hand_on = 0
            self.th.exit()
            self.th.isRun = False
            # Arducam_adapter_board.select_channel('A')
            win = Capture()
            r = win.showModal()
            print('메인 : 쓰레드 시작')
            self.th.isRun = True
            self.th.start()
        # if Arducam_adapter_board.camOk == False:
        #     QMessageBox.critical(self.centralwidget, "카메라 에러", "시스템을 리부팅하세요")   

    
    def CloseEvent(self, event):
        print("X is clicked")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #MainWindow.showMaximized()
    sys.exit(app.exec_())

