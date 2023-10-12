#! usr/bin/env python
# -*- coding:utf-8 -*-
# AtmosphericCorrection for Landsat8

import glob
import json

import xml.dom.minidom  # 读取xml格式的影像头文件


import numpy as np
from Py6S import *
from osgeo import gdal

import datetime
from osgeo.gdalconst import GA_ReadOnly
from PyQt5.QtCore import QThread,pyqtSignal
import os

##子线程.图像大气校正
class  CorrectGFThread(QThread):
    correct_GF1 = pyqtSignal(str)  # 设置触发信号传递的参数数据类型,这里是字符串
    InputFilename = ""
    OutputFilename=""


    def __init__(self):
        super(CorrectGFThread, self).__init__()

    def MeanDEM(self,pointUL, pointDR):
        '''
        计算影像所在区域的平均高程.
        '''
        script_path = os.path.split(os.path.realpath(__file__))[0]
        dem_path = os.path.join(script_path, "GMTED2km.tif")

        try:
            DEMIDataSet = gdal.Open(dem_path)
        except Exception as e:
            pass

        DEMBand = DEMIDataSet.GetRasterBand(1)
        geotransform = DEMIDataSet.GetGeoTransform()
        # DEM分辨率
        pixelWidth = geotransform[1]
        pixelHight = geotransform[5]

        # DEM起始点：左上角，X：经度，Y：纬度
        originX = geotransform[0]
        originY = geotransform[3]

        # 研究区左上角在DEM矩阵中的位置
        yoffset1 = int((originY - pointUL['lat']) / pixelWidth)
        xoffset1 = int((pointUL['lon'] - originX) / (-pixelHight))

        # 研究区右下角在DEM矩阵中的位置
        yoffset2 = int((originY - pointDR['lat']) / pixelWidth)
        xoffset2 = int((pointDR['lon'] - originX) / (-pixelHight))

        # 研究区矩阵行列数
        xx = xoffset2 - xoffset1
        yy = yoffset2 - yoffset1
        # 读取研究区内的数据，并计算高程
        DEMRasterData = DEMBand.ReadAsArray(xoffset1, yoffset1, xx, yy)

        MeanAltitude = np.mean(DEMRasterData)
        return MeanAltitude

    def AtmosphericCorrection(self,BandId, metedata, config, SatelliteID, SensorID):
        #                      波段，全球气象数据，json文件，卫星名字，传感器类型
        # 读取头文件
        dom = xml.dom.minidom.parse(metedata)
        # 6S模型
        s = SixS()
        # 传感器类型 自定义
        s.geometry = Geometry.User()

        s.geometry.solar_z = 90 - float(dom.getElementsByTagName('SolarZenith')[0].firstChild.data)
        s.geometry.solar_a = float(dom.getElementsByTagName('SolarAzimuth')[0].firstChild.data)
        # s.geometry.view_z = float(dom.getElementsByTagName('SatelliteZenith')[0].firstChild.data)
        # s.geometry.view_a = float(dom.getElementsByTagName('SatelliteAzimuth')[0].firstChild.data)
        # 亲测，假设垂直照射，效果最好。
        s.geometry.view_z = 0
        s.geometry.view_a = 0

        # 日期
        DateTimeparm = dom.getElementsByTagName('CenterTime')[0].firstChild.data
        DateTime = DateTimeparm.split(' ')
        Date = DateTime[0].split('-')
        s.geometry.month = int(Date[1])
        s.geometry.day = int(Date[2])

        # 中心经纬度
        TopLeftLat = float(dom.getElementsByTagName('TopLeftLatitude')[0].firstChild.data)
        TopLeftLon = float(dom.getElementsByTagName('TopLeftLongitude')[0].firstChild.data)
        TopRightLat = float(dom.getElementsByTagName('TopRightLatitude')[0].firstChild.data)
        TopRightLon = float(dom.getElementsByTagName('TopRightLongitude')[0].firstChild.data)
        BottomRightLat = float(dom.getElementsByTagName('BottomRightLatitude')[0].firstChild.data)
        BottomRightLon = float(dom.getElementsByTagName('BottomRightLongitude')[0].firstChild.data)
        BottomLeftLat = float(dom.getElementsByTagName('BottomLeftLatitude')[0].firstChild.data)
        BottomLeftLon = float(dom.getElementsByTagName('BottomLeftLongitude')[0].firstChild.data)
        ImageCenterLat = (TopLeftLat + TopRightLat + BottomRightLat + BottomLeftLat) / 4

        # 大气模式类型
        if ImageCenterLat > -15 and ImageCenterLat < 15:
            s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.Tropical)

        if ImageCenterLat > 15 and ImageCenterLat < 45:
            if s.geometry.month > 4 and s.geometry.month < 9:
                s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeSummer)
            else:
                s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeWinter)

        if ImageCenterLat > 45 and ImageCenterLat < 60:
            if s.geometry.month > 4 and s.geometry.month < 9:
                s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.SubarcticSummer)
            else:
                s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.SubarcticWinter)

        # 气溶胶类型大陆
        s.aero_profile = AtmosProfile.PredefinedType(AeroProfile.Continental)

        # 下垫面类型
        s.ground_reflectance = GroundReflectance.HomogeneousLambertian(0.36)

        # 550nm气溶胶光学厚度,对应能见度为40km
        s.aot550 = 0.14497

        # 通过研究区的范围去求DEM高度。
        pointUL = dict()
        pointDR = dict()
        pointUL["lat"] = max(TopLeftLat, TopRightLat, BottomRightLat, BottomLeftLat)
        pointUL["lon"] = min(TopLeftLon, TopRightLon, BottomRightLon, BottomLeftLon)
        pointDR["lat"] = min(TopLeftLat, TopRightLat, BottomRightLat, BottomLeftLat)
        pointDR["lon"] = max(TopLeftLon, TopRightLon, BottomRightLon, BottomLeftLon)
        meanDEM = (self.MeanDEM(pointUL, pointDR)) * 0.001

        # 研究区海拔、卫星传感器轨道高度
        s.altitudes = Altitudes()
        s.altitudes.set_target_custom_altitude(meanDEM)
        s.altitudes.set_sensor_satellite_level()

        # 中心波长（Central Wavelength）简称CL
        # 波谱范围（Spectrum Range）简称SR
        # 波谱响应函数（Spectral Response Function)srf

        # 校正波段（根据波段名称）
        if BandId == 1:
            SRFband = config["Parameter"][SatelliteID][SensorID]["SRF"]["1"]
            s.wavelength = Wavelength(0.450, 0.520, SRFband)

        elif BandId == 2:
            SRFband = config["Parameter"][SatelliteID][SensorID]["SRF"]["2"]

            s.wavelength = Wavelength(0.520, 0.590, SRFband)

        elif BandId == 3:
            SRFband = config["Parameter"][SatelliteID][SensorID]["SRF"]["3"]

            s.wavelength = Wavelength(0.630, 0.690, SRFband)

        elif BandId == 4:
            SRFband = config["Parameter"][SatelliteID][SensorID]["SRF"]["4"]
            s.wavelength = Wavelength(0.770, 0.890, SRFband)

        s.atmos_corr = AtmosCorr.AtmosCorrLambertianFromReflectance(-0.1)

        # 运行6s大气模型
        s.run()
        xa = s.outputs.coef_xa
        xb = s.outputs.coef_xb
        xc = s.outputs.coef_xc
        # x = s.outputs.values
        return (xa, xb, xc)

    def RadiometricCalibration(self,bandid, ImageType, SatelliteID, SensorID, Year, config):
        if SatelliteID[0:3] == "GF1":
            if SensorID[0:3] == "WFV":
                Gain = config["Parameter"][SatelliteID][SensorID][Year]["gain"][bandid - 1]
                Bias = config["Parameter"][SatelliteID][SensorID][Year]["offset"][bandid - 1]
            else:
                Gain = config["Parameter"][SatelliteID][SensorID][Year][ImageType[0:3]]["gain"][bandid - 1]
                Bias = config["Parameter"][SatelliteID][SensorID][Year][ImageType[0:3]]["offset"][bandid - 1]
        else:
            if SensorID[0:3] == "WFV":
                Gain = config["Parameter"][SatelliteID][SensorID][Year]["gain"][bandid - 1]
                Bias = config["Parameter"][SatelliteID][SensorID][Year]["offset"][bandid - 1]
            else:

                Gain = config["Parameter"][SatelliteID][SensorID][ImageType][Year]["gain"][bandid - 1]
                Bias = config["Parameter"][SatelliteID][SensorID][ImageType][Year]["offset"][bandid - 1]

        return Gain, Bias

    def Block(self,Outfilename, infile):

        filename_split = infile.split("_")
        filename_split2 = filename_split[0].replace("\\", "/").split("/")
        SatelliteID = filename_split2[-1]  # GF1
        SensorID = filename_split[1]  # PMS1
        Year = filename_split[4][:4]
        config = json.load(
            open(os.path.join(os.path.split(os.path.realpath(__file__))[0], "RadiometricCorrectionParameter.json")))
        metedata = glob.glob(os.path.join(os.path.dirname(infile), "*MSS*.xml"))[0]
        DataSet = gdal.Open(infile, GA_ReadOnly)

        # global cols,rows,atcfiles
        cols = DataSet.RasterXSize
        rows = DataSet.RasterYSize

        # 设置输出波段
        Driver = DataSet.GetDriver()
        geoTransform1 = DataSet.GetGeoTransform()
        # GeoTransform[0]，左上角横坐标（应该是投影坐标）
        # GeoTransform[2]，行旋转
        # GeoTransform[1]，像元宽度(影像在水平空间的分辨率)
        # GeoTransform[3]，左上角纵坐标（应该是投影坐标）
        # GeoTransform[4]，列旋转
        # GeoTransform[5]，像元高度(影像在垂直空间的分辨率)，

        ListgeoTransform1 = list(geoTransform1)
        ListgeoTransform1[5] = -ListgeoTransform1[5]
        newgeoTransform1 = tuple(ListgeoTransform1)
        proj1 = DataSet.GetProjection()
        im_data = DataSet.GetRasterBand(1).ReadAsArray(0, 0, cols, rows)
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_Int16
        else:
            datatype = gdal.GDT_Float32

        outDataset = Driver.Create(Outfilename, cols, rows, 4, datatype)
        outDataset.SetGeoTransform(newgeoTransform1)

        outDataset.SetProjection(proj1)
        # 分别读取4个波段

        for bandid in range(1, 5):

            ReadBand = DataSet.GetRasterBand(bandid)
            outband = outDataset.GetRasterBand(bandid)
            outband.SetNoDataValue(-9999)
            # 获取对应波段的增益gain和偏移bias
            # print("123")
            # print(os.path.basename(infile))
            ImageType = os.path.basename(infile)[-9:-5]
            # print(ImageType)

            Gain, Bias = self.RadiometricCalibration(bandid, ImageType, SatelliteID, SensorID, Year, config)

            nBlockSize = 2048
            i = 0
            j = 0
            self.correct_GF1.emit("第%d波段校正......" % bandid)

            while i < rows:
                while j < cols:
                    # 保存分块大小
                    nXBK = nBlockSize
                    nYBK = nBlockSize

                    # 最后不够分块的区域，有多少读取多少
                    if i + nBlockSize > rows:
                        nYBK = rows - i
                    if j + nBlockSize > cols:
                        nXBK = cols - j

                    # 分块读取影像
                    Image = ReadBand.ReadAsArray(j, i, nXBK, nYBK)

                    # 辐射定标
                    atcImage = np.where(Image > 0, Image * Gain + Bias, -9999)

                    # # 获取大气校正系数
                    AtcCofa, AtcCofb, AtcCofc = self.AtmosphericCorrection(bandid, metedata, config, SatelliteID, SensorID)
                    # 基于辐射传输方程的大气校正 （）6S

                    y = np.where(atcImage != -9999, AtcCofa * atcImage - AtcCofb, -9999)
                    atcImage = np.where(y != -9999, (y / (1 + y * AtcCofc)) * 10000, -9999)
                    # y = AtcCofa * outImage - AtcCofb
                    # Image_block_band = (y / (1 + y * AtcCofc)) * 10000
                    outband.WriteArray(atcImage, j, i)
                    j = j + nXBK

                j = 0
                i = i + nYBK
            self.correct_GF1.emit("第%d波段校正完成" % bandid)

    # if __name__ == "__main__":
        # os.environ['PROJ_LIB'] = r'D:\Anaconda\Ana\Lib\site-packages\pyproj\proj_dir\share\proj'
        # infile = r"H:\GF1ScoreImage\GF1_PMS1_E102.4_N24.7_20190127_L1A0003794985\GF1_PMS1_E102.4_N24.7_20190127_L1A0003794985-MSS1.tiff"
        # outFileName = r"H:\GF1ScoreImage\GF1_PMS1_E102.4_N24.7_20190127_L1A0003794985\GF1_PMS1_E102.4_N24.7_20190127_L1A0003794985-MSS1-6s.tiff"
        # Block(outFileName, infile)

    def run(self):
       start1 = datetime.datetime.now()
       self.Block(self.OutputFilename,self.InputFilename)
       end1 = datetime.datetime.now()
       self.correct_GF1.emit("end")
       self.correct_GF1.emit('运行结束，共用时 %s Seconds' % (end1 - start1))
