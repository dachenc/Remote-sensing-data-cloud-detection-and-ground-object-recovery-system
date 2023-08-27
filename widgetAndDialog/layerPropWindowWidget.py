import traceback
from qgis.core import QgsVectorLayer,QgsRasterLayer,QgsProject,QgsStyle,QgsSymbol,QgsWkbTypes,QgsSymbolLayer,Qgis,QgsFeatureRenderer
from qgis.gui import QgsRendererRasterPropertiesWidget,QgsSingleSymbolRendererWidget,QgsCategorizedSymbolRendererWidget
from PyQt5.QtCore import QModelIndex
from ui.layerPropWindow import Ui_LayerProp
from PyQt5.QtWidgets import QWidget,QDialog,QListWidgetItem,QTabBar
from QgisUtils import getRasterLayerAttrs,getVectorLayerAttrs

PROJECT = QgsProject.instance()

class LayerPropWindowWidgeter(QDialog, Ui_LayerProp):
    def __init__(self,layer,parent=None):
        """
        # tab 信息含义：
        0 栅格信息 1 矢量信息 2 栅格图层渲染 3 矢量图层渲染
        :param layer:
        :param parent:
        """
        super(LayerPropWindowWidgeter,self).__init__(parent)
        self.layer = layer
        self.parentWindow = parent
        self.setupUi(self)
        self.initUI()
        self.connectFunc()

    def initUI(self):
        layerbar = self.tabWidget.findChild(QTabBar)
        layerbar.hide()
        renderBar = self.comboTabWidget.findChild(QTabBar)
        renderBar.hide()
        self.listWidget.setCurrentRow(0)
        self.initInfomationTab()
        self.decideRasterNVector(0)

    def connectFunc(self):
        self.listWidget.itemClicked.connect(self.listWidgetItemClicked)
        self.okPb.clicked.connect(lambda : self.renderApplyPbClicked(needClose=True))
        self.cancelPb.clicked.connect( self.close )
        self.applyPb.clicked.connect(lambda : self.renderApplyPbClicked(needClose=False))
        self.vecterRenderCB.currentIndexChanged.connect(self.vecterRenderCBChanged)

    # 切换矢量渲染方式
    def vecterRenderCBChanged(self):
        self.comboTabWidget.setCurrentIndex(self.vecterRenderCB.currentIndex())

    def initInfomationTab(self):
        if type(self.layer) == QgsRasterLayer:
            rasterLayerDict = getRasterLayerAttrs(self.layer)
            self.rasterNameLabel.setText(rasterLayerDict['name'])
            self.rasterSourceLabel.setText(rasterLayerDict['source'])
            self.rasterMemoryLabel.setText(rasterLayerDict['memory'])
            self.rasterExtentLabel.setText(rasterLayerDict['extent'])
            self.rasterWidthLabel.setText(rasterLayerDict['width'])
            self.rasterHeightLabel.setText(rasterLayerDict['height'])
            self.rasterDataTypeLabel.setText(rasterLayerDict['dataType'])
            self.rasterBandNumLabel.setText(rasterLayerDict['bands'])
            self.rasterCrsLabel.setText(rasterLayerDict['crs'])
            self.rasterRenderWidget = QgsRendererRasterPropertiesWidget(self.layer, self.parentWindow.mapCanvas,parent=self)
            self.layerRenderLayout.addWidget(self.rasterRenderWidget)

        elif type(self.layer) == QgsVectorLayer:
            self.layer : QgsVectorLayer
            vectorLayerDict = getVectorLayerAttrs(self.layer)
            self.vectorNameLabel.setText(vectorLayerDict['name'])
            self.vectorSourceLabel.setText(vectorLayerDict['source'])
            self.vectorMemoryLabel.setText(vectorLayerDict['memory'])
            self.vectorExtentLabel.setText(vectorLayerDict['extent'])
            self.vectorGeoTypeLabel.setText(vectorLayerDict['geoType'])
            self.vectorFeatureNumLabel.setText(vectorLayerDict['featureNum'])
            self.vectorEncodingLabel.setText(vectorLayerDict['encoding'])
            self.vectorCrsLabel.setText(vectorLayerDict['crs'])
            self.vectorDpLabel.setText(vectorLayerDict['dpSource'])

            # single Render
            self.vectorSingleRenderWidget = QgsSingleSymbolRendererWidget(self.layer,QgsStyle.defaultStyle(),self.layer.renderer())
            self.singleRenderLayout.addWidget(self.vectorSingleRenderWidget)

            # category Render
            self.vectorCateGoryRenderWidget = QgsCategorizedSymbolRendererWidget(self.layer,QgsStyle.defaultStyle(),self.layer.renderer())
            self.cateRenderLayout.addWidget(self.vectorCateGoryRenderWidget)

    def decideRasterNVector(self,index):
        if index == 0:
            if type(self.layer) == QgsRasterLayer:
                self.tabWidget.setCurrentIndex(0)
            elif type(self.layer) == QgsVectorLayer:
                self.tabWidget.setCurrentIndex(1)
        elif index == 1:
            if type(self.layer) == QgsRasterLayer:
                self.tabWidget.setCurrentIndex(2)
            elif type(self.layer) == QgsVectorLayer:
                self.tabWidget.setCurrentIndex(3)


    def listWidgetItemClicked(self,item:QListWidgetItem):
        tempIndex = self.listWidget.indexFromItem(item).row()
        self.decideRasterNVector(tempIndex)


    def renderApplyPbClicked(self,needClose=False):
        if self.tabWidget.currentIndex() <= 1:
            print("没有在视图里，啥也不干")
        elif type(self.layer) == QgsRasterLayer:
            self.rasterRenderWidget : QgsRendererRasterPropertiesWidget
            self.rasterRenderWidget.apply()
        elif type(self.layer) == QgsVectorLayer:
            print("矢量渲染")
            #self.vectorRenderWidget : QgsSingleSymbolRendererWidget
            self.layer : QgsVectorLayer
            if self.comboTabWidget.currentIndex() == 0:
                renderer = self.vectorSingleRenderWidget.renderer()
            else:
                renderer = self.vectorCateGoryRenderWidget.renderer()
            self.layer.setRenderer(renderer)
            self.layer.triggerRepaint()
        self.parentWindow.mapCanvas.refresh()
        if needClose:
            self.close()


