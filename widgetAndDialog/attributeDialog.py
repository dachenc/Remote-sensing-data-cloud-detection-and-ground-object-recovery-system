# -*- coding: utf-8 -*-
# @Author  : yoyi
# @Time    : 2020/10/20 15:01
from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtWidgets import QDialog, QHBoxLayout,QDockWidget,QVBoxLayout,QDesktopWidget,QMessageBox
from qgis.core import QgsVectorLayerCache,QgsVectorLayer
from qgis.gui import QgsAttributeTableView, QgsAttributeTableModel, QgsAttributeTableFilterModel,QgsGui

class AttributeDialog(QDialog):
    def __init__(self, mainWindows,layer):
        #mainWindows : MainWindow
        super(AttributeDialog, self).__init__(mainWindows)
        self.mainWindows = mainWindows
        self.mapCanvas = self.mainWindows.mapCanvas
        self.layer : QgsVectorLayer = layer
        self.setObjectName("attrWidget"+self.layer.id())
        self.setWindowTitle("属性表:"+self.layer.name())
        vl = QHBoxLayout(self)
        self.tableView = QgsAttributeTableView(self)
        self.resize(800, 600)
        vl.addWidget(self.tableView)
        self.center()
        self.openAttributeDialog()
        QgsGui.editorWidgetRegistry().initEditors(self.mapCanvas)#如果不添加这，编辑状态下的属性表会直接卡死软件

    def center(self):
        # 获取屏幕的尺寸信息
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口的尺寸信息
        size = self.geometry()
        # 将窗口移动到指定位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def openAttributeDialog(self):
        #iface
        self.layerCache = QgsVectorLayerCache(self.layer, 10000)#设置图层的最大缓存
        self.tableModel = QgsAttributeTableModel(self.layerCache)
        self.tableModel.loadLayer()

        self.tableFilterModel = QgsAttributeTableFilterModel(self.mapCanvas, self.tableModel, parent=self.tableModel)
        self.tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)  #显示问题
        self.tableView.setModel(self.tableFilterModel)
        #self.tableView.edit()
        #print(self.tableView.currentIndex())
