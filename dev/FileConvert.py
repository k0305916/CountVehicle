# coding=utf-8
# import math
# import arcpy
# import datetime
# import os
# from simpledbf import Dbf5


# yourpath = "C:/Users/wushi/Desktop/experiment/paper1_new/demo/"

class FileConvert:
    def csvToShape(self, inputcsv):
        pass
        # attr = inputcsv.split('/')[-1].split('.')[0]
        # addXY =  attr + "_"
        # outShapefile = os.path.join(yourpath,attr + ".shp")
        # # print "Output shapefile path: %s" % outShapefile
        # if os.path.exists(outShapefile):
        #     return outShapefile
        # arcpy.MakeXYEventLayer_management(inputcsv, "longitude", "latitude", addXY,arcpy.SpatialReference(4326))
        # arcpy.CopyFeatures_management(addXY, outShapefile)
        # # print "Convert csv to shapfile complete! \n"
        # return outShapefile

    def convert(self):
        pass
        # inputcsv1 = yourpath + "demodata.csv"
        # join_features = yourpath + "taz.shp"
        # out_feature_class = yourpath + "ini/" +inputcsv1.split('/')[-1].split('.')[0] +"_spajoin.shp"
        # outpath1 = yourpath + "ini/" + inputcsv1.split('/')[-1].split('.')[0] +"_spajoin.csv"

        # target_features = csvToShape(inputcsv1)
        # arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,join_type="KEEP_COMMON")
        # arcpy.Delete_management(target_features)

        # dbf = Dbf5(out_feature_class.split('.')[0]+'.dbf')
        # df1 = dbf.to_dataframe()
        # df1.to_csv(outpath1,sep=',',mode='a',index=True)
        # arcpy.Delete_management(out_feature_class)
