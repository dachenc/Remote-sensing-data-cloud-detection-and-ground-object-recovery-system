from PyQt5.QtCore import QDir, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from ui.AtmosphericDialog import Ui_Dialog


class myAtomosphericDialog(QDialog, Ui_Dialog):
    myAtomsignel = pyqtSignal(str)  # 自定义信号
    def __init__(self, parent=None):

        # 通过super调用父类构造函数，创建QWidget窗体，这样self就是一个窗体对象了
        super(myAtomosphericDialog, self).__init__(parent)
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
        self.myAtomsignel.emit("大气校正")
        inpath=self.lineEdit_input.text()
        self.myAtomsignel.emit(inpath)
        outpath=self.lineEdit_output.text()
        self.myAtomsignel.emit(outpath)
        self.myAtomsignel.emit("end")
        self.close()

    def pushButton_cancel_clicked(self):
        self.close()

    def pushButton_InPath(self):
        curPath = QDir.currentPath()
        title = "选择输入文件夹"
        fileName = QFileDialog.getExistingDirectory(None, title, curPath)
        if (fileName == ""):
            QMessageBox.information(self, "提示", self.tr("没有选择影像文件！"))
            return
        self.lineEdit_input.setText(fileName)

    def pushButton_OutPath(self):
        curPath = QDir.currentPath()
        title = "选择输出文件夹"
        fileName = QFileDialog.getExistingDirectory(None, title, curPath)
        if (fileName == ""):
            QMessageBox.information(self, "提示", self.tr("没有选择输出文件！"))
            return
        self.lineEdit_output.setText(fileName)