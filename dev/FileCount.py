import os
from datetime import datetime
from FileOper import Vehicle


class FileCount:
    '计算空车数量'
    __filepath = ""
    __filecount = {}

    def __init__(self, filepath):
        self.__filepath = filepath

    def run(self):
        '解析文件，计算空车数量'
        f_read = open(self.__filepath)
        fristline = False
        last = -1
        for eachline in f_read:
            if not fristline:
                fristline = True
                continue

            value = eachline.replace('\n','').split(',')
            vehicle = Vehicle()
            vehicle.car_number = value[0]
            vehicle.trip_id = value[1]
            vehicle.datetime_record = value[2]
            vehicle.longitude = value[3]
            vehicle.latitude = value[4]
            vehicle.speed = value[5]
            vehicle.direction = value[6]
            vehicle.region = value[7]

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

    def outputfile(self):
        "输出文件"
        path, file = os.path.split(self.__filepath)
        name, extention = os.path.splitext(file)
        directory = path+'\\'+name+'_count'
        if not os.path.exists(directory):
            os.mkdir(directory)
        for _data in self.__filecount:
            outfile = open(directory+'\\'+_data+'.txt', 'wt')
            outfile.writelines(
                'retion,count\n')
            outfile.flush()
            for data in self.__filecount[_data]:
                outfile.writelines(data+','+
                                    str((self.__filecount[_data])[data])+'\n')
                outfile.flush()
            outfile.close()

