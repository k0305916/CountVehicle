import os


class Vehicle:
    '车辆结构数据'
    __car_number = ""
    __trip_id = ""
    __datetime_record = ""
    __longitude = ""
    __latitude = ""
    __speed = ""
    __direction = ""
    __region = ""

    def __init__(self, car_number, trip_id, datetime_record, longitude, latitude, speed, direction):
        self.__car_number = car_number
        self.__trip_id = trip_id
        self.__datetime_record = datetime_record
        self.__longitude = longitude
        self.__latitude = latitude
        self.__speed = speed
        self.__direction = direction

    def setregion(self, region):
        '设置区域'
        self.__region = region

    def getvalue(self):
        '返回数据'
        return [self.__car_number, self.__trip_id, self.__datetime_record, self.__longitude, self.__latitude, self.__speed, self.__direction, self.__region]


class FileOper:
    '处理文件的类'
    #额。。。不知道这样写是否正确。。。。。
    __outfile = open()
    __data = []

    def __init__(self, filepath):
        path, file = os.path.split(filepath)
        name, extention = os.path.splitext(file)
        self.outfile = open(path+name+"_convert"+extention, 'wt')
        self.outfile.writelines(
            'car_number,trip_id,datetime_record,longitude,latitude,speed,direction,region')

    def processfile(self, filepath):
        """
        处理文件：取出每行的数据，将其与arcgis的区域API结合，得到匹配区域。
        """
        f_read = open(filepath)
        fristline = False
        for eachline in f_read:
            if not fristline:
                fristline = True
                continue

            value = eachline.split(',')
            vehicle = Vehicle(value[0], value[1], value[2],
                              value[3], value[4], value[5], value[6])
            #通过arcgis+loction得到区域值
            region = "0"

            vehicle.setregion(region)
            self.__data.append(vehicle)

    def outputfile(self):
        '输出文件'
        for data in self.__data:
            value = data.getvalue
            self.__outfile.writelines(value[0]+','+value[1]+','+value[2]+','+value[3] +
                                      ','+value[4]+','+value[5]+','+value[6]+','+value[7]+','+value[8])

        self.__outfile.close()
