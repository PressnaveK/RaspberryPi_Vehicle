from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import RPi.GPIO as GPIO
from time import sleep

import cv2


class Ui_CONTROL(QWidget):
    def __init__(self):
        super(Ui_CONTROL,self).__init__()
        # Varibles
        self.n = 0
        self.start = False
        self.forward = True
        self.pwm_L = 0
        self.pwm_R = 0
        # Initializing pin_Mode
        self.Ena_R = 18
        self.In1 = 14
        self.In2 = 15
        
        self.Ena_L = 12
        self.In3 = 16
        self.In4 = 20
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        GPIO.setup(self.In3,GPIO.OUT)
        GPIO.setup(self.In4,GPIO.OUT)
        GPIO.setup(self.Ena_R,GPIO.OUT)
        GPIO.setup(self.Ena_L,GPIO.OUT)
        self.PWM_R = GPIO.PWM(self.Ena_R,1000)
        self.PWM_L = GPIO.PWM(self.Ena_L,1000)

        
        self.setObjectName("CONTROL")
        self.resize(1022, 717)
        self.lbl_Title = QtWidgets.QLabel(self)
        self.lbl_Title.setGeometry(QtCore.QRect(330, 0, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(24)
        self.lbl_Title.setFont(font)
        self.lbl_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Title.setObjectName("lbl_Title")
        self.lcd_left = QtWidgets.QLCDNumber(self)
        self.lcd_left.setGeometry(QtCore.QRect(770, 580, 171, 91))
        self.lcd_left.setObjectName("lcd_left")
        self.lcd_right = QtWidgets.QLCDNumber(self)
        self.lcd_right.setGeometry(QtCore.QRect(90, 580, 171, 91))
        self.lcd_right.setObjectName("lcd_right")
        self.lbl_M_L = QtWidgets.QLabel(self)
        self.lbl_M_L.setGeometry(QtCore.QRect(790, 550, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_M_L.setFont(font)
        self.lbl_M_L.setObjectName("lbl_M_L")
        self.lbl_M_R = QtWidgets.QLabel(self)
        self.lbl_M_R.setGeometry(QtCore.QRect(90, 540, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_M_R.setFont(font)
        self.lbl_M_R.setObjectName("lbl_M_R")
        self.lbl_mode = QtWidgets.QLabel(self)
        self.lbl_mode.setGeometry(QtCore.QRect(460, 50, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_mode.setFont(font)
        self.lbl_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mode.setObjectName("lbl_mode")


#VBL QVBoxLayout
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 80, 861, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.VBL = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.VBL.setContentsMargins(0, 0, 0, 0)
        self.VBL.setObjectName("VBL")

        self.FeedLabel = QLabel()
        self.FeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VBL.addWidget(self.FeedLabel)


        self.lbl_R = QtWidgets.QLabel(self)
        self.lbl_R.setGeometry(QtCore.QRect(790, 50, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_R.setFont(font)
        self.lbl_R.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_R.setObjectName("lbl_R")
        self.lbl_L = QtWidgets.QLabel(self)
        self.lbl_L.setGeometry(QtCore.QRect(80, 50, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_L.setFont(font)
        self.lbl_L.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_L.setObjectName("lbl_L")

#txt_Room Combobox keyPressEvent will be disable while making QCombobox or QTextEdit as enable
        self.txt_Room = QtWidgets.QComboBox(self)
        self.txt_Room.setGeometry(QtCore.QRect(470, 540, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txt_Room.setFont(font)
        self.txt_Room.setObjectName("txt_Room")
        self.txt_Room.addItems(["Room-1","Room-2","Room-3",])
        self.txt_Room.setEnabled(False)
        self.txt_Room.setVisible(False)

#btn_Manual
        self.btn_Manual = QtWidgets.QPushButton(self)
        self.btn_Manual.setGeometry(QtCore.QRect(40, 10, 181, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_Manual.setFont(font)
        self.btn_Manual.setObjectName("btn_Manual")
        self.btn_Manual.setEnabled(False)
        self.btn_Manual.setVisible(False)
        self.btn_Manual.clicked.connect(self.Manual)

        QtCore.QMetaObject.connectSlotsByName(self)


   
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("CONTROL", "Controller"))
        self.lbl_Title.setText(_translate("CONTROL", "MED VEHICLE"))
        self.lbl_M_L.setText(_translate("CONTROL", "LEFT MOTOR"))
        self.lbl_M_R.setText(_translate("CONTROL", "RIGHT MOTOR"))
        self.lbl_mode.setText(_translate("CONTROL", "BACKWARD"))
        self.lbl_R.setText(_translate("CONTROL", "RIGHT "))
        self.lbl_L.setText(_translate("CONTROL", "LEFT"))
        self.btn_Manual.setText(_translate("CONTROL", "FORCE TO MANUAL"))

        self.Video_Capture = Video_Cap()
        self.Video_Capture.start()
        self.Video_Capture.ImageUpdate.connect(self.ImgUpdateSlot)

    def ImgUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A:
            self.Auto()
        if e.key() == Qt.Key_R:
            self.Set_Mode()
        if e.key() == Qt.Key_S:
            self.Set_Start()
        if e.key() == Qt.Key_B:
            self.Set_Brake()
        if e.key() == Qt.Key_J:
            self.PWM_Increase_L()
        if e.key() == Qt.Key_K:
            self.PWM_Decrease_L()
        if e.key() == Qt.Key_F:
            self.PWM_Increase_R()
        if e.key() == Qt.Key_D:
            self.PWM_Decrease_R()
    def Set_GPIO(self):
        if self.forward == True:
            GPIO.output(self.In1,GPIO.HIGH)
            GPIO.output(self.In2,GPIO.LOW)
            GPIO.output(self.In3,GPIO.HIGH)
            GPIO.output(self.In4,GPIO.LOW)
        else:
            GPIO.output(self.In2,GPIO.HIGH)
            GPIO.output(self.In1,GPIO.LOW)
            GPIO.output(self.In4,GPIO.HIGH)
            GPIO.output(self.In3,GPIO.LOW)
            
    def Set_PWM(self):
        self.PWM_R.ChangeDutyCycle(self.pwm_R)
        self.PWM_L.ChangeDutyCycle(self.pwm_L)
        


    def Auto(self):
        self.txt_Room.setEnabled(True)
        self.txt_Room.setVisible(True)
        self.txt_Room.setFocus(True)
        self.btn_Manual.setEnabled(True)
        self.btn_Manual.setVisible(True)

    def Manual(self):
        self.txt_Room.setEnabled(False)
        self.txt_Room.setVisible(False)
        self.btn_Manual.setEnabled(False)
        self.btn_Manual.setVisible(False)

    def Set_Start(self):
        self.start = True
        self.forward = True
        self.pwm_L = 25
        self.pwm_R = 25
        self.lbl_mode.setText("FORWARD")
        self.lcd_left.display(self.pwm_L)
        self.lcd_right.display(self.pwm_R)
        self.Set_GPIO()
        self.PWM_R.start(25)
        self.PWM_L.start(25)
        
        
            

    def Set_Mode(self):
        if self.start == True :
            self.n += 1
            if self.n % 2 == 1:
                self.forward = False
                self.lbl_mode.setText("BACKWARD")
                self.pwm_L = 0
                self.pwm_R = 0
                self.lcd_left.display(self.pwm_L)
                self.lcd_right.display(self.pwm_R)
                
                
 
            else:
                self.forward = True
                self.lbl_mode.setText("FORWARD")
                self.pwm_L = 0
                self.pwm_R = 0
                self.lcd_left.display(self.pwm_L)
                self.lcd_right.display(self.pwm_R)
               
            self.Set_GPIO()
            self.Set_PWM()

            
    def Set_Brake(self):
        if self.start == True :
            self.n = 0
            self.forward = True
            self.lbl_mode.setText("FORWARD")
            self.pwm_L = 0
            self.pwm_R = 0
            self.lcd_left.display(self.pwm_L)
            self.lcd_right.display(self.pwm_R)
            self.Set_GPIO()
            self.Set_PWM()


    def PWM_Increase_R(self):
        if self.start == True :
            if self.pwm_R < 100:
                self.pwm_R += 5
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            else:
                self.pwm_R = 100
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            self.Set_GPIO()
            self.Set_PWM()

    def PWM_Increase_L(self):
        if self.start == True :
            if self.pwm_L < 100:
                self.pwm_L += 5
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            else:
                self.pwm_L = 100
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            self.Set_GPIO()
            self.Set_PWM()

    def PWM_Decrease_R(self):
        if self.start == True :
            if self.pwm_R > 0:
                self.pwm_R -= 5
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            else:
                self.pwm_R = 0
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            self.Set_GPIO()
            self.Set_PWM()

    def PWM_Decrease_L(self):
        if self.start == True :
            if self.pwm_L > 0:
                self.pwm_L -= 5
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            else:
                self.pwm_L = 0
                self.lcd_right.display(self.pwm_R)
                self.lcd_left.display(self.pwm_L)
            self.Set_GPIO()
            self.Set_PWM()


class Video_Cap(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret,frame = Capture.read()
            frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
            if ret:
                Image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                FlippedImg = cv2.flip(Image,1)
                ConvertToQt = QImage(FlippedImg.data,FlippedImg.shape[1],FlippedImg.shape[0],QImage.Format_RGB888)
                Pic = ConvertToQt.scaled(441,862,Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_CONTROL()
    ui.show()
    sys.exit(app.exec_())
