import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from ui.LandSat8_AtmosphericDialog import Ui_Dialog

class myAtomosphericDialog_Lan(QDialog, Ui_Dialog):

    myAtomsignel = pyqtSignal(str)  # 自定义信号
    myAtomsignel_index=pyqtSignal(str,str)

    def __init__(self, parent=None):

        # 通过super调用父类构造函数，创建QWidget窗体，这样self就是一个窗体对象了
        super(myAtomosphericDialog_Lan, self).__init__(parent)

        # 创建UI对象，私有属性__ui包含了可视化设计的UI窗体上的所有组件.
        self.setupUi(self)

        self.InitUI()  # 接口

    def InitUI(self):

        # 输入路径
        self.pushButton_input.clicked.connect(self.pushButton_InPath)
        #输出路径
        self.pushButton_output.clicked.connect(self.pushButton_OutPath)
        # cancel
        self.pushButton_cancel.clicked.connect(self.pushButton_cancel_clicked)
        # OK
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)


    def pushButton_ok_clicked(self):
        if (self.lineEdit_input.text()== ""):
            QMessageBox.information(self, "提示", self.tr("没有选择输入路径！"))
            return
        if (os.path.exists(self.lineEdit_input.text()) == False):
            QMessageBox.information(self, "提示", self.tr("输入路径不存在！"))
            return
        if (self.lineEdit_output.text()== ""):
            QMessageBox.information(self, "提示", self.tr("没有选择输出路径！"))
            return

        self.myAtomsignel.emit("LandSat-8辐射校正------")
        inpath=self.lineEdit_input.text()
        self.myAtomsignel.emit("输入路径为："+inpath)
        outpath=self.lineEdit_output.text()
        self.myAtomsignel.emit("输出路径为："+outpath)
        self.myAtomsignel.emit("star")
        self.myAtomsignel_index.emit(inpath,outpath)

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
        #curPath = QDir.currentPath()
        curPath =  r"E:\AARS\QGIS\Data"
        title = "选择文件夹"
        fileName= QFileDialog.getExistingDirectory(None,title, curPath)

        if os.path.exists(fileName)==True:
            if len(os.listdir(fileName)) == 0:
                self.lineEdit_output.setText(fileName)
            else:
                QMessageBox.information(self, "提示", self.tr("请选择空文件夹！"))
                return
        else:
            QMessageBox.information(self, "提示", self.tr("文件位置不存在！"))

        return

