#coding=utf-8
import os
import sys
import threading
import copy
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, wait
from FileOper import FileOper
from FileConvert import FileConvert
from FileCount import FileCount

#python中全局变量的注意点：
#http://blog.csdn.net/dongtingzhizi/article/details/8973569
#,'H:\\LiFan\\CountVehicle\\data\\0hunting\\p1\\402088.csv'
#FILELIST = [['H:/LiFan/CountVehicle/data/0hunting/demo/demodata.csv'],['H:/LiFan/CountVehicle/data/0hunting/demo/demodata1.csv']]
#FILELIST = []

FILELIST = [['E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141212/112151_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141212/112152_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141212/402085_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141212/402087_spajoin.csv'],
            ['E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/112153_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/112154_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/112155_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/402082_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/402083_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/402084_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/402088_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/402089_spajoin.csv',
             'E:/Business/Python/CountVehicle/CountVehicle/data/p2/20141211/402090_spajoin.csv']]

FILELISTCONVERT = []

FILERESULT = {}
MUTEX = threading.Lock()

def main():
    """
    input fie path
    """
    # if len(sys.argv) <= 2:
    #     print("请输入正确的参数：文件夹路径 shp文件夹路径")
    #     return

    # path = sys.argv[1]
    # directory = sys.argv[2]
    # if (not os.path.isdir(path)) or (not os.path.isdir(directory)):
    #     print("请输入正确的文件夹路径.")
    #     return
    directory = "H:/LiFan/CountVehicle/data/0hunting/demo/shp"
    path = "H:/LiFan/CountVehicle/data/0hunting/demo"

    # 获取该路径下的所有以.csv结尾的文件
    csvfiles = [os.path.join(r, file) for r, d, files in os.walk(
        path) for file in files if file.endswith(".csv")]
    cpucount = cpu_count()

    # #引入线程池进行多线程操作
    executor = ThreadPoolExecutor(cpucount)
    futures = []
    # for csv in csvfiles:
    #     futures.append(executor.submit(funccutfile, csv))
    # wait(futures)
    # futures.clear()
    futures[:] = []
    print("切分文件完成，开始进行文件转换.....")
    for filelist in FILELIST:
        for file in filelist:
            futures.append(executor.submit(fucconvertfile, file,directory))
        #有可能存在死了的情景。。。因此有个超时的设置
        wait(futures,10*1000)
        #python2.7不支持List.clear()
        #futures.clear()
        #b[:] = []采用这种方式清空
        futures[:] = []

        print("空车数量开始计算")
        dir = ""
        for file in FILELISTCONVERT:
            d, f = os.path.split(file)
            dir = d
            futures.append(executor.submit(funccountfile, file))
        wait(futures)
        #futures.clear()
        futures[:] = []
        countresult(dir)
        FILERESULT.clear()
        print("空车计算完成")

    print("所有空车数量全部计算完成")


def funccutfile(filepath):
    '生成文件操作对象，并处理'
    file = FileOper(filepath)
    file.cutfile()
    file.outputfile()
    MUTEX.acquire()
    FILELIST.append(file.getfilelist())
    MUTEX.release()


def fucconvertfile(filepath,directory):
    '转换文件'
    # file = FileConvert(filepath,directory)
    # file.convert()
    # MUTEX.acquire()
    # FILELISTCONVERT.append(file.getresultfile())
    # MUTEX.release()
    file = FileConvert(filepath,directory)
    MUTEX.acquire()
    FILELISTCONVERT.append(file.getresultfile1())
    MUTEX.release()

def funccountfile(filepath):
    '计算空车数量'
    file = FileCount(filepath)
    file.run()
    MUTEX.acquire()
    #将结果进行汇总
    global FILERESULT
    result = file.getresult()
    for _data in result:
        if _data not in FILERESULT:
            FILERESULT[_data] = copy.deepcopy(result[_data])
        else:
            for __data in result[_data]:
                if __data not in FILERESULT[_data]:
                    (FILERESULT[_data])[__data] = copy.deepcopy((result[_data])[__data])
                else:
                    (FILERESULT[_data])[__data] += (result[_data])[__data]
    MUTEX.release()

def countresult(directory):
    "输出文件"
    directory = directory+'\\count'
    if not os.path.exists(directory):
        os.mkdir(directory)
    for _data in FILERESULT:
        outfile = open(directory+'\\'+_data+'.txt', 'wt')
        outfile.writelines(
            'retion,count\n')
        outfile.flush()
        for data in FILERESULT[_data]:
            outfile.writelines(data+',' +
                               str((FILERESULT[_data])[data])+'\n')
            outfile.flush()
        outfile.close()


if __name__ == "__main__":
    sys.exit(main())
