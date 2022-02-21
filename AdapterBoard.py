import RPi.GPIO as gp
import os
import cv2 as cv 
import numpy as np
import time
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore


'''
                        "B":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x05",
                                "gpio_sta":[1,0,1],
                            },
'''

class MultiAdapter:
    camNum = 3
    adapter_info = {   "A":{   "i2c_cmd":"i2cset -y 0 0x70 0x00 0x04",
                                    "gpio_sta":[0,0,1],
                            },
 
                        "B":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x06",
                                "gpio_sta":[0,1,0],
                            },
                        "C":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x07",
                                "gpio_sta":[1,1,0],
                            },
                     } 
    
    width = 320*2
    height = 240*2
    cam_i = 0

    font                   = cv.FONT_HERSHEY_PLAIN
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 1
    factor  = 20
    texture = 0
    frame = []
    black = []
    data = []
    capture_now = 0
    camOk = False
    gpio_sel_0 = 7
    gpio_sel_1 = 11
    gpio_sel_2 = 12

    
    def __init__(self):
        self.camera = cv.VideoCapture(0)
 
        gp.setwarnings(False)

        gp.setmode(gp.BCM)
        self.gpio_sel_0 = 4
        self.gpio_sel_1 = 17
        self.gpio_sel_2 = 18
   
        '''
        gp.setmode(gp.BOARD)
        
        self.gpio_sel_0 = 7
        self.gpio_sel_1 = 11
        self.gpio_sel_2 = 12   
        
        '''
        gp.setup(self.gpio_sel_0, gp.OUT)
        gp.setup(self.gpio_sel_1,gp.OUT)
        gp.setup(self.gpio_sel_2,gp.OUT)  

    def choose_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        os.system(channel_info["i2c_cmd"]) # i2c write
        
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(self.gpio_sel_0, gpio_sta[0])
        gp.output(self.gpio_sel_1, gpio_sta[1])
        gp.output(self.gpio_sel_2, gpio_sta[2])

    def select_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        gpio_sta = channel_info["gpio_sta"] # gpio write
        
        gp.output(self.gpio_sel_0, gpio_sta[0])
        gp.output(self.gpio_sel_1, gpio_sta[1])
        gp.output(self.gpio_sel_2, gpio_sta[2])

    def init(self):
        if self.camOk == False:
            self.frame = np.zeros(((self.height), self.width, 3), dtype= np.uint8)
            #self.black = np.zeros(((self.height+self.factor)*2, self.width*2, 3), dtype= np.uint8)
            #self.texture = Texture.create(size=(self.width*2, (self.height+self.factor)*2), colorfmt="rgb")
            for i in range(self.camNum):
                self.choose_channel(chr(65+i)) 
                self.camera.set(3, self.width)
                self.camera.set(4, self.height)
                ret, self.frame = self.camera.read()
                if ret == True:
                    print("camera %s init OK" %(chr(65+ i)))
                    #pname = "image_"+ chr(65+i)+".jpg"
                    #cv.imwrite(pname,self.frame)
                    time.sleep(0.05)
                else:
                    self.camOk = False 
                    return
            self.camOk = True
        else:
            print("camera is already initialized")

    def preview2(self):
        self.camera.read()
        ret, self.frame = self.camera.read()
        if ret:
            self.frame = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB) 
            h,w,c = self.frame.shape
            qImg = QtGui.QImage(self.frame.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            self.pixmap = QtGui.QPixmap.fromImage(qImg)

        else:
            print("cannot read frame.")
        return ret


    def saveCapture(self):
        self.camera.read()
        ret, self.frame = self.camera.read()
        self.jpgname = "data/"+"image_"+ chr(65+self.cam_i)+ time.strftime('%y-%m-%d %H:%M:%S')+".jpg"
        cv.imwrite(self.jpgname,self.frame)
        print("camera %s capture" %(chr(65+self.cam_i)))
        #time.sleep(0.2)
    
    def preview(self):

        self.select_channel(chr(65+self.cam_i))
        self.frame.dtype=np.uint8
        self.camera.read()
        ret, self.frame = self.camera.read()
        if ret == False:
            print("camera %s read fail" %(chr(65+self.cam_i)))


        '''
        if self.cam_i == 0:
            self.black[self.factor:self.factor+self.height, 0:self.width, :] = self.frame
            bottomLeftCornerOfText = (self.factor,self.factor)
            index = chr(65+self.cam_i)
        elif self.cam_i == 1:
            self.black[self.factor:self.factor+self.height, self.width:self.width*2,:] = self.frame
            bottomLeftCornerOfText = (self.factor+self.width, self.factor)
            index = chr(65+self.cam_i)
        elif self.cam_i == 2:
            self.black[self.factor*2+self.height:self.factor*2+self.height*2, 0:self.width,:] = self.frame
            bottomLeftCornerOfText = (self.factor, self.factor*2+self.height)
            index = chr(65+self.cam_i)
        elif self.cam_i == 3:
            self.black[self.factor*2+self.height:self.factor*2+self.height*2, self.width:self.width*2,:] = self.frame
            bottomLeftCornerOfText = (self.factor+self.width, self.factor*2+self.height)
            index = chr(65+self.cam_i)
       
        cv.putText(self.black,'CAM '+index, bottomLeftCornerOfText, self.font, self.fontScale,self.fontColor,self.lineType)
        
        
        data = self.black.tobytes()
        self.texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgb")
        '''
        #self.data = self.frame.tobytes()
        
        #self.texture.blit_buffer(self.data, bufferfmt="ubyte", colorfmt="rgb")
        
        cv.imshow("Preview",self.frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            del self.frame
            self.camera.release()
            cv.destroyAllWindows()        
       
            
        #print("camera %s capture" %(chr(65+self.cam_i)))
        #pname = "image_"+ chr(65+self.cam_i)+ time.strftime('%y-%m-%d %H:%M:%S')+".jpg"
        #cv.imwrite(pname,self.frame)
        #time.sleep(0.2)
        
        self.cam_i = self.cam_i+1
        if self.cam_i==self.camNum:
            self.cam_i = 0

        '''
        if self.capture_now == 1:
            for i in range(self.camNum):
                self.choose_channel(chr(65+i)) 
                #self.camera.set(3, self.width)
                #self.camera.set(4, self.height)
                #ret, self.frame = self.camera.read()
                #ret, self.frame = self.camera.read()
                print("camera %s capture" %(chr(65+i)))
                pname = "image_"+ chr(65+i)+ time.strftime('%y-%m-%d %H:%M:%S')+".jpg"
                
               # cv.imshow(pname,self.frame)
                cv.imwrite(pname,self.frame)
                
                time.sleep(0.5)

            self.capture_now = 2
        '''


    def camera_stop(self):
        del self.frame
        #del self.black 
        self.camera.release()
            


        

