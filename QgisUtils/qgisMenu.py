from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu, QAction,QMessageBox
from qgis._core import QgsMapLayerType
from qgis.core import QgsLayerTreeNode, QgsLayerTree,  QgsProject,QgsMapLayer,QgsLayerTreeGroup
from qgis.gui import QgsLayerTreeViewMenuProvider, QgsLayerTreeView, QgsLayerTreeViewDefaultActions, QgsMapCanvas
import traceback

from widgetAndDialog import AttributeDialog
from widgetAndDialog.layerPropWindowWidget import LayerPropWindowWidgeter

PROJECT = QgsProject.instance()

class menuProvider(QgsLayerTreeViewMenuProvider):
    def __init__(self,mainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layerTreeView: QgsLayerTreeView = mainWindow.layerTreeView
        self.mapCanvas: QgsMapCanvas = mainWindow.mapCanvas
        self.mainWindows = mainWindow

    def createContextMenu(self) -> QtWidgets.QMenu:
        try:
            menu = QMenu()
            self.actions : QgsLayerTreeViewDefaultActions = self.layerTreeView.defaultActions()
            if not self.layerTreeView.currentIndex().isValid():
                # 清除图层 deleteAllLayer
                actionDeleteAllLayer = QAction('清除图层', menu)
                actionDeleteAllLayer.triggered.connect(lambda: self.deleteAllLayer())
                menu.addAction(actionDeleteAllLayer)

                menu.addAction('展开所有图层',self.layerTreeView.expandAllNodes)
                menu.addAction('折叠所有图层',self.layerTreeView.collapseAllNodes)
                return menu

            if len(self.layerTreeView.selectedLayers()) > 1:
                # 添加组
                self.actionGroupSelected = self.actions.actionGroupSelected()
                menu.addAction(self.actionGroupSelected)

                actionDeleteSelectedLayers = QAction('删除选中图层',menu)
                actionDeleteSelectedLayers.triggered.connect(self.deleteSelectedLayer)
                menu.addAction(actionDeleteSelectedLayers)

                return menu

            node: QgsLayerTreeNode = self.layerTreeView.currentNode()
            if node:
                if QgsLayerTree.isGroup(node):
                    group: QgsLayerTreeGroup = self.layerTreeView.currentGroupNode()
                    self.actionRenameGroup = self.actions.actionRenameGroupOrLayer(menu)
                    menu.addAction(self.actionRenameGroup)
                    actionDeleteGroup = QAction('删除组', menu)
                    actionDeleteGroup.triggered.connect(lambda: self.deleteGroup(group))
                    menu.addAction(actionDeleteGroup)
                elif QgsLayerTree.isLayer(node):
                    self.actionMoveToTop = self.actions.actionMoveToTop(menu)
                    menu.addAction(self.actionMoveToTop)
                    self.actionZoomToLayer = self.actions.actionZoomToLayer(self.mapCanvas, menu)
                    menu.addAction(self.actionZoomToLayer)

                    layer: QgsMapLayer = self.layerTreeView.currentLayer()

                    if layer.type() == QgsMapLayerType.VectorLayer:
                        actionOpenAttributeDialog = QAction('打开属性表', menu)
                        actionOpenAttributeDialog.triggered.connect(lambda: self.openAttributeDialog(layer))
                        menu.addAction(actionOpenAttributeDialog)

                    actionOpenLayerProp = QAction('图层属性', menu)
                    actionOpenLayerProp.triggered.connect(lambda : self.openLayerPropTriggered(layer))
                    menu.addAction(actionOpenLayerProp)

                    actionDeleteLayer = QAction("删除图层",menu)
                    actionDeleteLayer.triggered.connect(lambda : self.deleteLayer(layer))
                    menu.addAction(actionDeleteLayer)


                return menu

        except:
            print(traceback.format_exc())

    def openAttributeDialog(self, layer):
        ad = AttributeDialog(self.mainWindows, layer)
        ad.show()

    def openLayerPropTriggered(self,layer):
        try:
            self.lp = LayerPropWindowWidgeter(layer, self.mainWindows)
            print(type(self.lp))
            self.lp.show()
        except:
            print(traceback.format_exc())

    def updateRasterLayerRenderer(self,widget,layer):
        print("change")
        layer.setRenderer(widget.renderer())
        self.mapCanvas.refresh()

    def deleteSelectedLayer(self):
        deleteRes = QMessageBox.question(self.mainWindows, '信息', "确定要删除所选图层？", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if deleteRes == QMessageBox.Yes:
            layers = self.layerTreeView.selectedLayers()
            for layer in layers:
                self.deleteLayer(layer)

    def deleteAllLayer(self):
        if len(PROJECT.mapLayers().values()) == 0:
            QMessageBox.about(None, '信息', '您的图层为空')
        else:
            deleteRes = QMessageBox.question(self.mainWindows, '信息', "确定要删除所有图层？", QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
            if deleteRes == QMessageBox.Yes:
                for layer in PROJECT.mapLayers().values():
                        self.deleteLayer(layer)

    def deleteGroup(self,group:QgsLayerTreeGroup):
        deleteRes = QMessageBox.question(self.mainWindows, '信息', "确定要删除组？", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if deleteRes == QMessageBox.Yes:
            layerTreeLayers  = group.findLayers()
            for layer in layerTreeLayers:
                self.deleteLayer(layer.layer())
        PROJECT.layerTreeRoot().removeChildNode(group)

    def deleteLayer(self,layer):
        PROJECT.removeMapLayer(layer)
        self.mapCanvas.refresh()
        return 0