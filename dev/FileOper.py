import os


class Vehicle:
    '车辆结构数据'
    car_number = ""
    trip_id = ""
    datetime_record = ""
    longitude = ""
    latitude = ""
    speed = ""
    direction = ""
    region = ""


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
            vehicle = Vehicle()
            vehicle.car_number = value[0]
            vehicle.trip_id = value[1]
            vehicle.datetime_record = value[2]
            vehicle.longitude = value[3]
            vehicle.latitude = value[4]
            vehicle.speed = value[5]
            vehicle.direction = value[6]
            #通过arcgis+loction得到区域值
            region = "0"

            vehicle.region = region
            self.__data.append(vehicle)

    def outputfile(self):
        '输出文件'
        for data in self.__data:
            self.__outfile.writelines(data.car_number+',' +
                                      data.trip_id+',' +
                                      data.datetime_record+',' +
                                      data.longitude+',' +
                                      data.latitude+',' +
                                      data.speed+',' +
                                      data.direction+',' +
                                      data.region)

        self.__outfile.close()
