# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'innail.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import AdapterBoard 
import time
import os
import cv2 as cv 
import numpy as np  
import RPi.GPIO as GPIO
import board
import adafruit_mlx90614

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from capture import Capture
from uploading import Uploading
from qrreport import Qrreport
from functools import partial
import errno

Arducam_adapter_board = AdapterBoard.MultiAdapter()
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
            if Arducam_adapter_board.camOk == False:
                Arducam_adapter_board.init()
                Arducam_adapter_board.select_channel('A')
            
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

       

        font_label = QtGui.QFont()
        font_label.setPointSize(32)
        font_label.setBold(True)

        self.intro = QtWidgets.QLabel(self.centralwidget)
        self.intro.setGeometry(QtCore.QRect(50, 10, 700, 71)) 
        self.intro.setFont(font_label)
        self.intro.setObjectName("intro")

        self.temperature = QtWidgets.QLabel(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(200, 200, 400, 300)) 
        self.temperature.setFont(font_label)
        self.temperature.setObjectName("temperature")

        self.temperature_val = QtWidgets.QLabel(self.centralwidget)
        self.temperature_val.setGeometry(QtCore.QRect(400, 200, 500, 300)) 
        self.temperature_val.setFont(font_label)
        self.temperature_val.setObjectName("temperature_val")

        font_label_l = QtGui.QFont()
        font_label_l.setPointSize(120)
        font_label_l.setBold(True)

        self.countdown = QtWidgets.QLabel(self.centralwidget)
        self.countdown.setGeometry(QtCore.QRect(350, 100, 500, 200)) 
        self.countdown.setFont(font_label_l)
        self.countdown.setObjectName("countdown")

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

        GPIO.setup(self.pirPin, GPIO.IN, GPIO.PUD_UP)

        # # The MLX90614 only works at the default I2C bus speed of 100kHz.
        # # A higher speed, such as 400kHz, will not work.
        self.i2c = board.I2C()
        self.mlx = adafruit_mlx90614.MLX90614(self.i2c)
                
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
    

 
        self.intro.setText(_translate("MainWindow", "손을 올려 놓으면 측정이 시작 됩니다."))
        self.temperature.setText(_translate("MainWindow", "체온 : "))
        self.temperature_val.setText(_translate("MainWindow", "00"))
        self.countdown.setText(_translate("MainWindow", "5"))

    def onButtonClicked(self):
        if Arducam_adapter_board.camOk == False:
            time.sleep(1)
        Arducam_adapter_board.select_channel('A')
        Arducam_adapter_board.capture_init()

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
        print("Ambent Temp: ", self.mlx.ambient_temperature)
        print("Object Temp: ", self.mlx.object_temperature)

        floatTemp = float(self.mlx.object_temperature)

        tempAdjust = float(round(floatTemp + 1.7,1))

        _translate = QtCore.QCoreApplication.translate
        self.temperature_val.setText(_translate("MainWindow", str(tempAdjust)))
        self.countdown.setText(_translate("MainWindow", str(5 - self.hand_on)))

        self.cnt = self.cnt +1
        if GPIO.input(self.pirPin) !=  GPIO.LOW:
            print ("Motion detected!" +str(self.cnt))
            self.hand_on = self.hand_on+1

        else:
            print ("No motion"+str(self.cnt))
            self.hand_off = self.hand_off +1
            if self.hand_off > 6:
                self.hand_off = 0
                self.hand_on = 0
        if self.hand_on >6 :
            self.hand_off = 0
            self.hand_on = 0
            self.th.exit()
            self.th.isRun = False
            Arducam_adapter_board.select_channel('A')
            Arducam_adapter_board.capture_init()

            win = Capture()
            r = win.showModal(Arducam_adapter_board)
            if r==1:
                upload = Uploading()
                r2 = upload.showModal(Arducam_adapter_board)
                gotoInnail = Qrreport(upload.id_val)
                r3 = gotoInnail.showModal()



            print('메인 : 쓰레드 시작')
            self.th.isRun = True
            self.th.start()
        if Arducam_adapter_board.camOk == False:
            QMessageBox.critical(self.centralwidget, "카메라 에러", "시스템을 리부팅하세요")   

    
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

