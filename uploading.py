import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QProgressBar
import time
import requests
import uuid

class uploadThread(QThread):
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
 
            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
            self.threadEvent.emit(self.n)
            self.n += 1
            self.isRun = False 
          
            files_A =   open(self.main.adapter.jpgname[0], 'rb' ) 
            files_B =   open(self.main.adapter.jpgname[1], 'rb' )
            files_C =   open(self.main.adapter.jpgname[2], 'rb' )
            # 파이썬 딕셔너리 형식으로 file 설정 
            upload = [('file' , files_A), ('file_' , files_B), ('file__', files_C) ] 
            #upload = { 'file' : files } 
            self.main.id_val = uuid.uuid4().hex
            datas = {
                "id__":self.main.id_val,
                "file_list":"file file_ file__"
            }
            print(self.main.id_val)
            #res =  requests.post('http://127.0.0.1:8000/report/', files = upload )
            res =  requests.post('http://192.168.17.20:8000/report2/', files = upload, data = datas )
            #res =  requests.post('http://192.168.13.4:8000/report2/', files = upload, data = datas)
            #res =  requests.post('http://10.100.86.44:8000/report2/', files = upload, data = datas)
            #res =  requests.post('http://172.168.200.140:8000/report2/', files = upload, data =(datas))
            #res =  requests.post('http://innail.linkerverse.net/report2/', files = upload, data = datas )    
            print ( res.content ) 
            self.main.uploadfinish = 1

class Uploading(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('링커버스 닥터 분석')
        #self.setGeometry(100, 100, 200, 100)
        self.resize(800, 480)
        layout = QVBoxLayout()
        #layout.addStretch(1)
        layout_h1 = QHBoxLayout()
        
        font_notice= QtGui.QFont()
        font_notice.setPointSize(26)
        font_notice.setBold(True)
        
        self.label_notice=QLabel("촬영이 완료되었습니다. \n손을 빼셔도 됩니다.")
        self.label_notice.setFont(font_notice)
        layout_h1.addWidget(self.label_notice, alignment=Qt.AlignCenter)
        layout.addLayout(layout_h1)
        
        layout_H = QHBoxLayout()
        
        pixmap = QPixmap("faust_github.jpg")
        self.lbl_img = QLabel()
        self.lbl_img.setFixedSize(240,180)
        self.lbl_img.setPixmap(pixmap)
        
        pixmap2 = QPixmap("faust_github.jpg")
        self.lbl_img2 = QLabel()
        self.lbl_img2.setFixedSize(240,180)
        self.lbl_img2.setPixmap(pixmap2)
        
        pixmap3 = QPixmap("faust_github.jpg")
        self.lbl_img3 = QLabel()
        self.lbl_img3.setFixedSize(240,180)
        self.lbl_img3.setPixmap(pixmap3)
        
        layout_H.addWidget(self.lbl_img)
        layout_H.addWidget(self.lbl_img2)
        layout_H.addWidget(self.lbl_img3)
        
        layout.addLayout(layout_H)
        
        layout_h2 = QHBoxLayout()
        self.label_ready=QLabel("이제 인네일 닥터가 \n 분석을 준비합니다.")
        self.label_ready.setFont(font_notice)
        layout_h2.addWidget(self.label_ready, alignment=Qt.AlignCenter)
        layout.addLayout(layout_h2)
        
        self.pbar = QProgressBar(self)
        #self.pbar.setGeometry(30, 40, 200, 25)
        layout.addWidget(self.pbar)

        layout.addStretch(1)
        self.setLayout(layout)
        
         #쓰레드 인스턴스 생성
        self.th = uploadThread(self)
        #쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.uploadthreadEventHandler)
        print('threadEventHandler : 쓰레드 시작')
        self.th.isRun = True
        self.th.start()
        
        self.timer = QBasicTimer()
        self.step = 0
        self.uploadfinish = 0
        self.timer.start(200, self)
      
    def uploadthreadEventHandler(self, n):
        print("uploadthreadEventHandler")
        
        # if self.th.n ==100:
        #     self.uploadfinish = 1
        # if self.th.n ==110:
        #     self.th.exit()
        #     self.th.isRun = False  
        #     #self.close()
        #     #self.accept()
            
    def timerEvent(self, e):
        if self.step >= 100:
            if self.step >= 110:
                self.timer.stop()
                self.accept()
            self.step = self.step +1
            return
        
        if self.step == 99:
            self.step = self.step + self.uploadfinish
        else:
            self.step = self.step +1
        self.pbar.setValue(self.step)
        
    def showModal(self, _adapter):
        self.adapter = _adapter

        if self.adapter.save_cnt > 0:
            pixmap = QPixmap(self.adapter.jpgname[0])
            pixmap=pixmap.scaledToHeight(120)
            self.lbl_img.setFixedSize(240,180)
            self.lbl_img.setPixmap(pixmap)
            
        if self.adapter.save_cnt > 1:
            pixmap = QPixmap(self.adapter.jpgname[1])
            pixmap=pixmap.scaledToHeight(120)
            self.lbl_img2.setFixedSize(240,180)
            self.lbl_img2.setPixmap(pixmap)

        if self.adapter.save_cnt > 2:
            pixmap = QPixmap(self.adapter.jpgname[2])
            pixmap=pixmap.scaledToHeight(120)
            self.lbl_img3.setFixedSize(240,180)
            self.lbl_img3.setPixmap(pixmap)

        return super().exec_()