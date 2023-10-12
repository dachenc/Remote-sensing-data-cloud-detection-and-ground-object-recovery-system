import os
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from ui.LandSat8_BandcomDialog import Ui_Dialog

class myBandcomDialog_Lan(QDialog, Ui_Dialog):

    myAtomsignel = pyqtSignal(str)  # 自定义信号
    myAtomsignel_index=pyqtSignal(str,str,list)

    def __init__(self, parent=None):

        # 通过super调用父类构造函数，创建QWidget窗体，这样self就是一个窗体对象了
        super(myBandcomDialog_Lan, self).__init__(parent)

        # 创建UI对象，私有属性__ui包含了可视化设计的UI窗体上的所有组件.
        self.setupUi(self)

        self.checkBox_1.stateChanged.connect(self.checkbox_1_state_changed)
        self.checkBox_2.stateChanged.connect(self.checkbox_2_state_changed)
        self.checkBox_3.stateChanged.connect(self.checkbox_3_state_changed)
        self.checkBox_4.stateChanged.connect(self.checkbox_4_state_changed)
        self.checkBox_5.stateChanged.connect(self.checkbox_5_state_changed)
        self.checkBox_6.stateChanged.connect(self.checkbox_6_state_changed)
        self.checkBox_7.stateChanged.connect(self.checkbox_7_state_changed)
        self.checkBox_8.stateChanged.connect(self.checkbox_8_state_changed)
        self.checkBox_9.stateChanged.connect(self.checkbox_9_state_changed)
        self.checkBox_10.stateChanged.connect(self.checkbox_10_state_changed)
        self.checkBox_11.stateChanged.connect(self.checkbox_11_state_changed)

        self.band=[]#保存复选框里的波段号

        self.InitUI()  # 接口

    def InitUI(self):
        if self.checkBox_1.isChecked() :
            self.band.append(1)
        if self.checkBox_2.isChecked() :
            self.band.append(2)
        if self.checkBox_3.isChecked() :
            self.band.append(3)
        if self.checkBox_4.isChecked() :
            self.band.append(4)
        if self.checkBox_5.isChecked() :
            self.band.append(5)
        if self.checkBox_6.isChecked() :
            self.band.append(6)
        if self.checkBox_7.isChecked() :
            self.band.append(7)
        if self.checkBox_8.isChecked() :
            self.band.append(8)
        if self.checkBox_9.isChecked() :
            self.band.append(9)
        if self.checkBox_10.isChecked() :
            self.band.append(10)
        if self.checkBox_11.isChecked() :
            self.band.append(11)
        # 输入路径
        self.pushButton_input.clicked.connect(self.pushButton_InPath)
        #输出路径
        self.pushButton_output.clicked.connect(self.pushButton_OutPath)
        # cancel
        self.pushButton_cancel.clicked.connect(self.pushButton_cancel_clicked)
        # OK
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)


    def checkbox_1_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(1)
            else:
                self.band.remove(1)

    def checkbox_2_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(2)
            else:
                self.band.remove(2)

    def checkbox_3_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(3)
            else:
                self.band.remove(3)

    def checkbox_4_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(4)
            else:
                self.band.remove(4)
    def checkbox_5_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(5)
            else:
                self.band.remove(5)
    def checkbox_6_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(6)
            else:
                self.band.remove(6)

    def checkbox_7_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(7)
            else:
                self.band.remove(7)
    def checkbox_8_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(8)
            else:
                self.band.remove(8)
    def checkbox_9_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(9)
            else:
                self.band.remove(9)
    def checkbox_10_state_changed(self,state):
            if state == Qt.Checked:
                self.band.append(10)
            else:
                self.band.remove(10)
    def checkbox_11_state_changed(self,state):

            if state == Qt.Checked:
                self.band.append(11)
            else:
                self.band.remove(11)

    def pushButton_ok_clicked(self):
        if (len(self.band)==0):
            QMessageBox.information(self, "提示", self.tr("没有选择合成波段！"))
            return
        if (len(self.band) == 1):
            QMessageBox.information(self, "提示", self.tr("只选择了单个波段！无需合成！"))
            return
        if (self.lineEdit_input.text()== ""):
            QMessageBox.information(self, "提示", self.tr("没有选择输入路径！"))
            return
        if (os.path.exists(self.lineEdit_input.text()) == False):
            QMessageBox.information(self, "提示", self.tr("输入路径不存在！"))
            return
        if (self.lineEdit_output.text()== ""):
            QMessageBox.information(self, "提示", self.tr("没有选择输出路径！"))
            return

        self.myAtomsignel.emit("LandSat-8波段合成------")
        inpath=self.lineEdit_input.text()
        self.myAtomsignel.emit("输入路径为："+inpath)
        outpath=self.lineEdit_output.text()
        self.myAtomsignel.emit("输出路径为："+outpath)
        self.myAtomsignel.emit("star")
        self.band.sort()
        self.myAtomsignel.emit("所选波段号为：" + str(self.band))
        self.myAtomsignel_index.emit(inpath,outpath,self.band)

        self.close()


    def pushButton_cancel_clicked(self):
        self.close()

    def pushButton_InPath(self):
        title = "选择文件夹"
         #curPath = QDir.currentPath()
        curPath=r"E:\AARS\QGIS\Data"
        fileName = QFileDialog.getExistingDirectory(None, title, curPath)
        if (fileName == ""):
            QMessageBox.information(self, "提示", self.tr("没有选择影像文件！"))
            return
        self.lineEdit_input.setText(fileName)

    def pushButton_OutPath(self):
        # curPath = QDir.currentPath()
        curPath = r"E:\AARS\QGIS\Data"
        title = "选择输出路径"
        filt = "*.tif"
        fileName, flt = QFileDialog.getSaveFileName(self, title, curPath, filt)
        if (fileName == ""):
            QMessageBox.information(self, "提示", self.tr("没有选择输出路径！"))
            return
        self.lineEdit_output.setText(fileName)

