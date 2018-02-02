# coding=utf-8
import os


class Vehicle:
    '车辆结构数据'
    def __init__(self):
        self.car_number = ""
        self.trip_id = ""
        self.datetime_record = ""
        self.longitude = ""
        self.latitude = ""
        self.speed = ""
        self.direction = ""
        self.region = ""


class FileOper:
    '处理文件的类'
    def __init__(self, filepath):
        self.__filepath = filepath
        self.__filelist = []
        self.__data = {}

    def cutfile(self):
        """
        处理文件：取出每行的数据，将其与arcgis的区域API结合，得到匹配区域。
        """
        f_read = open(self.__filepath)
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

            if vehicle.trip_id in self.__data:
                self.__data[vehicle.trip_id].append(vehicle)
            else:
                self.__data[vehicle.trip_id] = [vehicle]

    def outputfile(self):
        '输出文件'
        path, file = os.path.split(self.__filepath)
        name, extention = os.path.splitext(file)
        directory = path+'\\'+name
        if not os.path.exists(directory):
            os.mkdir(directory)
        for _data in self.__data:
            outfile = open(directory+'\\'+_data+extention, 'wt')
            outfile.writelines(
                'car_number,trip_id,datetime_record,longitude,latitude,speed,direction\n')
            outfile.flush()
            self.__filelist.append(directory+'\\'+_data+extention)
            for data in self.__data[_data]:
                outfile.writelines(data.car_number+',' +
                                   data.trip_id+',' +
                                   data.datetime_record+',' +
                                   data.longitude+',' +
                                   data.latitude+',' +
                                   data.speed+',' +
                                   data.direction)
                outfile.flush()
            outfile.close()

    def getfilelist(self):
        return self.__filelist
