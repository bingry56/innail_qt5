# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(735, 443)
        self.Retry_2 = QtWidgets.QPushButton(Dialog)
        self.Retry_2.setEnabled(True)
        self.Retry_2.setGeometry(QtCore.QRect(10, 10, 511, 331))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Retry_2.setFont(font)
        self.Retry_2.setObjectName("Retry_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(550, 20, 161, 31))
        self.label.setObjectName("label")
        self.Upload_3 = QtWidgets.QPushButton(Dialog)
        self.Upload_3.setGeometry(QtCore.QRect(550, 50, 161, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Upload_3.setFont(font)
        self.Upload_3.setObjectName("Upload_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(550, 160, 161, 31))
        self.label_2.setObjectName("label_2")
        self.Upload_4 = QtWidgets.QPushButton(Dialog)
        self.Upload_4.setGeometry(QtCore.QRect(550, 190, 161, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Upload_4.setFont(font)
        self.Upload_4.setObjectName("Upload_4")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(550, 300, 161, 31))
        self.label_3.setObjectName("label_3")
        self.Upload_5 = QtWidgets.QPushButton(Dialog)
        self.Upload_5.setGeometry(QtCore.QRect(550, 330, 161, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Upload_5.setFont(font)
        self.Upload_5.setObjectName("Upload_5")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(10, 360, 511, 61))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Retry = QtWidgets.QPushButton(self.splitter)
        self.Retry.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Retry.setFont(font)
        self.Retry.setObjectName("Retry")
        self.Upload = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Upload.setFont(font)
        self.Upload.setObjectName("Upload")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "촬영"))
        self.Retry_2.setText(_translate("Dialog", "다시찍기"))
        self.label.setText(_translate("Dialog", "Camera A"))
        self.Upload_3.setText(_translate("Dialog", "업로드"))
        self.label_2.setText(_translate("Dialog", "Camera A"))
        self.Upload_4.setText(_translate("Dialog", "업로드"))
        self.label_3.setText(_translate("Dialog", "Camera A"))
        self.Upload_5.setText(_translate("Dialog", "업로드"))
        self.Retry.setText(_translate("Dialog", "다시찍기"))
        self.Upload.setText(_translate("Dialog", "업로드"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

