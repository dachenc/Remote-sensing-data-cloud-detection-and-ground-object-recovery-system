# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LandSat8_BandcomDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton_input = QtWidgets.QPushButton(Dialog)
        self.pushButton_input.setGeometry(QtCore.QRect(10, 30, 91, 31))
        self.pushButton_input.setObjectName("pushButton_input")
        self.lineEdit_input = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_input.setGeometry(QtCore.QRect(110, 30, 281, 31))
        self.lineEdit_input.setText("")
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.pushButton_output = QtWidgets.QPushButton(Dialog)
        self.pushButton_output.setGeometry(QtCore.QRect(10, 190, 91, 31))
        self.pushButton_output.setObjectName("pushButton_output")
        self.lineEdit_output = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_output.setGeometry(QtCore.QRect(110, 190, 281, 31))
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(140, 250, 93, 28))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(290, 250, 93, 28))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.checkBox_1 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_1.setGeometry(QtCore.QRect(10, 120, 41, 19))
        self.checkBox_1.setObjectName("checkBox_1")
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setEnabled(True)
        self.checkBox_2.setGeometry(QtCore.QRect(70, 120, 41, 19))
        self.checkBox_2.setTabletTracking(False)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_3.setGeometry(QtCore.QRect(130, 120, 41, 19))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_4.setGeometry(QtCore.QRect(190, 120, 41, 19))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_10 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_10.setGeometry(QtCore.QRect(190, 150, 51, 19))
        self.checkBox_10.setObjectName("checkBox_10")
        self.checkBox_9 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_9.setGeometry(QtCore.QRect(130, 150, 41, 19))
        self.checkBox_9.setObjectName("checkBox_9")
        self.checkBox_8 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_8.setGeometry(QtCore.QRect(70, 150, 41, 19))
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_7 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_7.setGeometry(QtCore.QRect(10, 150, 41, 19))
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_5 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_5.setGeometry(QtCore.QRect(250, 120, 41, 19))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_11 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_11.setGeometry(QtCore.QRect(260, 150, 51, 19))
        self.checkBox_11.setObjectName("checkBox_11")
        self.checkBox_6 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_6.setGeometry(QtCore.QRect(310, 120, 41, 19))
        self.checkBox_6.setObjectName("checkBox_6")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 80, 141, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "LandSat-8波段合成"))
        self.pushButton_input.setText(_translate("Dialog", "输入路径"))
        self.pushButton_output.setText(_translate("Dialog", "输出路径"))
        self.pushButton_ok.setText(_translate("Dialog", "OK"))
        self.pushButton_cancel.setText(_translate("Dialog", "cancel"))
        self.checkBox_1.setText(_translate("Dialog", "B1"))
        self.checkBox_2.setText(_translate("Dialog", "B2"))
        self.checkBox_3.setText(_translate("Dialog", "B3"))
        self.checkBox_4.setText(_translate("Dialog", "B4"))
        self.checkBox_10.setText(_translate("Dialog", "B10"))
        self.checkBox_9.setText(_translate("Dialog", "B9"))
        self.checkBox_8.setText(_translate("Dialog", "B8"))
        self.checkBox_7.setText(_translate("Dialog", "B7"))
        self.checkBox_5.setText(_translate("Dialog", "B5"))
        self.checkBox_11.setText(_translate("Dialog", "B11"))
        self.checkBox_6.setText(_translate("Dialog", "B6"))
        self.label.setText(_translate("Dialog", "选择要合成的波段："))
from resources import MyRc_rc