#主窗口
import sys
import traceback

from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog, QMessageBox, QStatusBar, QLabel, \
    QComboBox
from qgis._core import QgsLayerTreeModel, QgsProject, QgsCoordinateReferenceSystem, QgsMapSettings
from qgis._gui import QgsLayerTreeMapCanvasBridge, QgsMapCanvas, QgsLayerTreeView

from QgisUtils import QgisLayerUtils
from QgisUtils.qgisMenu import menuProvider
from ui.MyFirstWin import Ui_MainWindow



PROJECT = QgsProject.instance()


class myMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # 通过super调用父类构造函数，创建QWidget窗体，这样self就是一个窗体对象了
        super(myMainWin, self).__init__(parent)
        # 创建UI对象，私有属性__ui包含了可视化设计的UI窗体上的所有组件.
        # self = Pre001.Ui_MainWindow()
        self.setupUi(self)

        # 1 初始化图层树
        vl = QVBoxLayout(self.dockWidgetContents)
        self.layerTreeView = QgsLayerTreeView(self)
        vl.addWidget(self.layerTreeView)
        # 2 初始化地图画布
        self.mapCanvas = QgsMapCanvas(self)
        hl = QHBoxLayout(self.frame)#地图画布目前只有一个frame，先设为QHBoxLayout水平布局
        hl.setContentsMargins(0, 0, 0, 0)  # 设置周围间距
        hl.addWidget(self.mapCanvas)
        # 3 设置图层树风格
        self.model = QgsLayerTreeModel(PROJECT.layerTreeRoot(), self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)  # 允许图层节点重命名
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)  # 允许图层拖拽排序
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)  # 允许改变图层节点可视性
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)  # 展示图例
        self.model.setAutoCollapseLegendNodes(10)  # 当节点数大于等于10时自动折叠
        self.layerTreeView.setModel(self.model)
        # 4 建立图层树与地图画布的桥接
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(PROJECT.layerTreeRoot(), self.mapCanvas, self)
        # 5 初始加载影像
        self.firstAdd = True#判断地图初始打开
        # 6 允许拖拽文件
        self.setAcceptDrops(True)
        # 7 图层树右键菜单创建
        self.rightMenuProv = menuProvider(self)
        self.layerTreeView.setMenuProvider(self.rightMenuProv)
        # 8 error catch
        self.old_hook = sys.excepthook
        sys.excepthook = self.catch_exceptions
        # 9 提前给予基本CRS
        self.mapCanvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))

        # 10 状态栏控件
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('color: black; border: none')
        self.statusXY = QLabel('{:<40}'.format(''))  # x y 坐标状态
        self.statusBar.addWidget(self.statusXY, 1)
        self.statusScaleLabel = QLabel('比例尺')
        self.statusScaleComboBox = QComboBox(self)
        self.statusScaleComboBox.setFixedWidth(120)
        self.statusScaleComboBox.addItems(
            ["1:500", "1:1000", "1:2500", "1:5000", "1:10000", "1:25000", "1:100000", "1:500000", "1:1000000"])
        self.statusScaleComboBox.setEditable(True)
        self.statusBar.addWidget(self.statusScaleLabel)
        self.statusBar.addWidget(self.statusScaleComboBox)
        self.statusCrsLabel = QLabel(
            f"坐标系: {self.mapCanvas.mapSettings().destinationCrs().description()}-{self.mapCanvas.mapSettings().destinationCrs().authid()}")
        self.statusBar.addWidget(self.statusCrsLabel)

        self.setStatusBar(self.statusBar)
        self.initUI()  # 接口



    def initUI(self):
        self.connectFunction()#链接open的槽函数
        self.mapCanvas.destinationCrsChanged.connect(self.showCrs)#改变状态栏
        self.mapCanvas.xyCoordinates.connect(self.showXY)#显示XY坐标
        self.mapCanvas.scaleChanged.connect(self.showScale)#动态刷新比例尺
        self.statusScaleComboBox.editTextChanged.connect(self.changeScaleForString)#手动输入比例尺

    def changeScaleForString(self, str):
        try:
            left, right = str.split(":")[0], str.split(":")[-1]
            if int(left) == 1 and int(right) > 0 and int(right) != int(self.mapCanvas.scale()):
                self.mapCanvas.zoomScale(int(right))
                self.mapCanvas.zoomWithCenter()
        except:
            print(traceback.format_stack())


    def showScale(self, scale):
        self.statusScaleComboBox.setEditText(f"1:{int(scale)}")


    def showXY(self, point):
        x = point.x()
        y = point.y()
        self.statusXY.setText(f'{x:.6f}, {y:.6f}')

    def showCrs(self):
        mapSetting: QgsMapSettings = self.mapCanvas.mapSettings()
        self.statusCrsLabel.setText(
            f"坐标系: {mapSetting.destinationCrs().description()}-{mapSetting.destinationCrs().authid()}")

    def catch_exceptions(self, ty, value, trace):
        """
            捕获异常，并弹窗显示
        :param ty: 异常的类型
        :param value: 异常的对象
        :param traceback: 异常的traceback
        """
        traceback_format = traceback.format_exception(ty, value, trace)
        traceback_string = "".join(traceback_format)
        QMessageBox.about(self, 'error', traceback_string)
        self.old_hook(ty, value, trace)

    # 拖拽事件
    def dragEnterEvent(self, fileData):
        if fileData.mimeData().hasUrls():
            fileData.accept()  # 鼠标放开函数事件
        else:
            fileData.ignore()

    # 发现拖拽了文件后，将会触发下面的函数
    def dropEvent(self, fileData):
        mimeData: QMimeData = fileData.mimeData()
        filePathList = [u.path()[1:] for u in mimeData.urls()]
        for filePath in filePathList:
            filePath: str = filePath.replace("/", "//")
            if filePath.split(".")[-1] in ["tif", "TIF", "tiff", "TIFF", "GTIFF", "png", "jpg", "pdf"]:
                 self.addRasterLayer(filePath)
            elif filePath.split(".")[-1] in ["shp", "SHP", "gpkg", "geojson", "kml"]:
                 self.addVectorLayer(filePath)
            elif filePath == "":
                 pass
            else:
                QMessageBox.about(self, '警告', f'{filePath}为不支持的文件类型，目前支持栅格影像和shp矢量')


    def connectFunction(self):
        self.action_OpenRaster.triggered.connect(self.actionOpenRasterTriggered)
        self.action_OpenShp.triggered.connect(self.actionOpenShpTriggered)

    def actionOpenRasterTriggered(self):
        #curPath = QDir.currentPath()
        curPath = r"E:\AARS\QGIS\Data"
        title = "选择影像文件"
        filt = "*.tif *.tiff *.TIF *.TIFF *.png *.jpg ;;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        if (fileName == ""):
            QMessageBox.information(self, "提示", self.tr("没有选择影像路径！"))
            return
        else:
            self.addRasterLayer(fileName)

    def actionOpenShpTriggered(self):
        curPath = r"E:\AARS\QGIS\Data"
        title = "选择矢量文件"
        filt = "*.shp *.SHP;;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        if (fileName == ""):
            QMessageBox.information(self, "提示", self.tr("没有选择影像路径！"))
            return
        else:
            self.addVectorLayer(fileName)


    def addRasterLayer(self, rasterFilePath):#加载栅格数据
        rasterLayer = QgisLayerUtils.readRasterFile(rasterFilePath)
        if self.firstAdd:
            QgisLayerUtils.addMapLayer(rasterLayer, self.mapCanvas, True)
            self.firstAdd = False
        else:
            QgisLayerUtils.addMapLayer(rasterLayer, self.mapCanvas)

    def addVectorLayer(self, vectorFilePath):#加载矢量数据
        vectorLayer = QgisLayerUtils.readVectorFile(vectorFilePath)
        if self.firstAdd:
             QgisLayerUtils.addMapLayer(vectorLayer, self.mapCanvas, True)
             self.firstAdd = False
        else:
             QgisLayerUtils.addMapLayer(vectorLayer, self.mapCanvas)

        # __ui是私有属性，在类外部创建对象，是无法通过对象访问窗体上的组件的，为了访问组件，可以定义接口，实现功能

