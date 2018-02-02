# coding=utf-8
import math
#import arcpy
import datetime
import os
#from simpledbf import Dbf5


class FileConvert:
    def __init__(self, filepath, directory):
        self.__filepath = filepath
        self.__directory = directory
        self.__outputfile = ""

    def __csvToShape(self, inputcsv):
        path, file = os.path.split(self.__filepath)
        name, extention = os.path.splitext(file)
        #attr = inputcsv.split('/')[-1].split('.')[0]
        attr = name
        addXY = attr + "_"
        outShapefile = self.__directory+'/'+name+'/'+ attr + ".shp"
        print("Output shapefile path: %s", outShapefile)
        if os.path.exists(outShapefile):
            return outShapefile
        arcpy.MakeXYEventLayer_management(
            inputcsv, "longitude", "latitude", addXY, arcpy.SpatialReference(4326))
        arcpy.CopyFeatures_management(addXY, outShapefile)
        print("Convert csv to shapfile complete! \n")
        return outShapefile

    def convert(self):
        path, file = os.path.split(self.__filepath)
        name, extention = os.path.splitext(file)
        inputcsv1 = self.__filepath
        join_features = self.__directory + "/taz.shp"
        #使用name作为文件夹名称，若统一使用ini的话，多线程状态下会产生__csvToShape函数错误
        directory = self.__directory+'/'+name+'/'
        if not os.path.exists(directory):
            os.mkdir(directory)
        else:
            self.__removedir(directory)
            os.mkdir(directory)
        out_feature_class = os.path.join(directory,name + "_spajoin.shp")
        #将输出文件至filepath同级目录下
        outpath1 = os.path.join(path,name+ "_spajoin.csv")
        self.__outputfile = outpath1

        target_features = self.__csvToShape(inputcsv1)
        arcpy.SpatialJoin_analysis(
            target_features, join_features, out_feature_class, join_type="KEEP_COMMON")
        #arcpy.Delete_management(target_features)

        dbf = Dbf5(out_feature_class.split('.')[0]+'.dbf')
        #df1 = dbf.to_dataframe()
        #使用以下的to_csv会出错，细节不清楚
        #dbf.to_csv(outpath1, sep=',', mode='a', index=True)
        dbf.to_csv(outpath1)
        print("Convert dbf to csv complete! \n")
        #arcpy.Delete_management(out_feature_class)

    def getresultfile(self):
        return self.__outputfile

    def getresultfile1(self):
        return self.__filepath

    def __removedir(self,directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


