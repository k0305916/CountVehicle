# coding=utf-8
import os
from datetime import datetime

class Vehicle:
    '车辆结构数据'
    def __init__(self):
        self.Join_Count = ""
        self.TARGET_FID = ""
        self.car_number = ""
        self.trip_id = ""
        self.datetime_record = ""
        self.longitude = ""
        self.latitude = ""
        self.speed = ""
        self.direction = ""
        self.taz = ""


class FileCount:
    '计算空车数量'
    # __filepath = ""
    # __filecount = {}

    def __init__(self, filepath):
        self.__filepath = filepath
        self.__filecount={}

    def run(self):
        '解析文件，计算空车数量'
        f_read = open(self.__filepath)
        fristline = False
        last = -1
        for eachline in f_read:
            if not fristline:
                fristline = True
                continue

            value = eachline.replace('\n', '').split(',')
            vehicle = Vehicle()
            vehicle.Join_Count = value[0]
            vehicle.TARGET_FID = value[1]
            vehicle.car_number = value[2]
            vehicle.trip_id = value[3]
            vehicle.datetime_record = value[4]
            vehicle.longitude = value[5]
            vehicle.latitude = value[6]
            vehicle.speed = value[7]
            vehicle.direction = value[8]
            vehicle.region = value[9]

            #这个地方需要判断是否要求是在同一个时间段
            if int(vehicle.region) == last:
                continue

            timerange = self.__time(vehicle.datetime_record)

            if timerange in self.__filecount:
                region = self.__filecount[timerange]
                if vehicle.region in region:
                        region[vehicle.region] += 1
                else:
                    region[vehicle.region] = 1
            else:
                self.__filecount[timerange] = {vehicle.region: 1}
            last = int(vehicle.region)

    def __time(self, time):
        timeobj = datetime.strptime(time, '%Y/%m/%d %H:%M')
        if timeobj.hour >= 0 and timeobj.hour < 4:
            return '1'
        elif timeobj.hour >= 4 and timeobj.hour < 8:
            return '2'
        elif timeobj.hour >= 8 and timeobj.hour < 12:
            return '3'
        elif timeobj.hour >= 12 and timeobj.hour < 16:
            return '4'
        elif timeobj.hour >= 16 and timeobj.hour < 20:
            return '5'
        else:
            return '6'
    def getresult(self):
        return self.__filecount
