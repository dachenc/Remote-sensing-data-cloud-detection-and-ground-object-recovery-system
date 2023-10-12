from qgis.PyQt import QtCore
from qgis.core import QgsApplication
from PyQt5.QtCore import Qt
from MyMainWin import myMainWin

if __name__ == '__main__':
    #提供qgis安装路径
    #QgsApplication.setPrefixPath('C:/qgis322/apps/qgis-ltr', True)
    QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # 创建对QgsApplication设置的引用第二个参数为True启用GUI，这是一个自定义应用程序
    app = QgsApplication([], True)

    # 中文翻译
    t = QtCore.QTranslator()
    t.load(r'zh-Hans.qm')
    app.installTranslator(t)

    app.initQgis()
    mainWindow = myMainWin()#创建窗口
    mainWindow.show()
    app.exec_()
    # 脚本完成后，调用exitQgis（）从内存中删除提供者和图层注册
    app.exitQgis()
