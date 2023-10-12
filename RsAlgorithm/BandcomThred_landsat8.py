#! usr/bin/env python
# -*- coding:utf-8 -*-
# AtmosphericCorrection for Landsat8

import os
import numpy as np
from osgeo import gdal
import datetime
from osgeo.gdalconst import GA_ReadOnly
from PyQt5.QtCore import QThread,pyqtSignal


##子线程.图像波段合成
class  BandcomLanThread(QThread):
    bandcom_landsat8 = pyqtSignal(str)  # 设置触发信号传递的参数数据类型,这里是字符串
    InputFilename = ""
    OutputFilename = ""
    bandid=[]

    def __init__(self):
        super(BandcomLanThread, self).__init__()

    def readtif(self,filename):
        gdal.AllRegister()
        dataset = gdal.Open(filename, GA_ReadOnly)  # 打开文件
        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数
        bands = dataset.RasterCount
        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息

        if bands == 1:
            image = np.zeros((im_height, im_width))
            band = dataset.GetRasterBand(1)
            image[:, :] = band.ReadAsArray(0, 0, im_width, im_height)
            del dataset
        else:
            image = np.zeros((bands, im_height, im_width))
            for b in range(bands):
                band = dataset.GetRasterBand(b + 1)
                image[b, :, :] = band.ReadAsArray(0, 0, im_width, im_height)
            del dataset
        return image, im_width, im_height, im_geotrans, im_proj

    def write_img(self,filename, im_proj, im_geotrans, im_data):
        # gdal数据类型包括
        # gdal.GDT_Byte,
        # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        # gdal.GDT_Float32, gdal.GDT_Float64
        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

        # 创建文件
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:  # 如果是单波段数据
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
        del dataset

    def bandcom(self,inputdir, outputfile, band):  # 123456 10
        num = len(band)
        data = []
        for i in range(num):
            EndName = ("B" + str(band[i]) + ".TIF")
            for f in os.listdir(inputdir):
                if f.endswith(EndName) == True:
                    img, im_width, im_height, im_geotrans, im_proj = self.readtif(inputdir + os.sep + f)
            data.append(img)
        data = np.array(data)
        self.write_img(outputfile, im_proj, im_geotrans, data)


    def run(self):
       start1 = datetime.datetime.now()

       self.bandcom(self.InputFilename, self.OutputFilename,self.bandid)
       end1 = datetime.datetime.now()
       self.bandcom_landsat8.emit("end")
       self.bandcom_landsat8.emit('运行结束，共用时 %s Seconds' % (end1 - start1))
