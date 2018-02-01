import os
import sys
import threading
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, wait
from FileOper import FileOper
from FileConvert import FileConvert
from FileCount import FileCount

FILELIST = []
FILELISTCONVERT = [['E:\\Business\\Python\\CountVehicle\\CountVehicle\\data\\112151.csv',
                    'E:\\Business\\Python\\CountVehicle\\CountVehicle\\data\\402088.csv']]

FILERESULT = []
MUTEX = threading.Lock()

def main():
    """
    input fie path
    """
    # if len(sys.argv) <= 2:
    #     print("请输入正确的参数：文件夹路径 shp文件夹路径")
    #     return

    # path = sys.argv[1]
    # if os.path.isdir(path) != True:
    #     print("请输入正确的文件夹路径.")
    #     return

    # #获取该路径下的所有以.csv结尾的文件
    # csvfiles = [os.path.join(r, file) for r, d, files in os.walk(
    #     path) for file in files if file.endswith(".csv")]
    # cpucount = cpu_count()

    # #引入线程池进行多线程操作
    executor = ThreadPoolExecutor(1)
    futures = []
    # for csv in csvfiles:
    #     futures.append(executor.submit(funccutfile, csv))
    # wait(futures)
    # futures.clear()
    # print("切分文件完成，开始进行文件转换.....")
    # for filelist in FILELIST:
    #     for file in filelist:
    #         futures.append(executor.submit(fucconvertfile, file))
    # wait(futures)
    # futures.clear()
    # print("文件转换完成，开始计算空车数量.....")
    for filelist in FILELISTCONVERT:
        path, f = os.path.split(filelist[0])
        for file in filelist:
            futures.append(executor.submit(funccountfile, file))
        wait(futures)
        futures.clear()
        countresult(path)
        FILERESULT.clear()
    print("空车计算完成，请检查。")

def funccutfile(filepath):
    '生成文件操作对象，并处理'
    file = FileOper(filepath)
    file.cutfile()
    file.outputfile()
    MUTEX.acquire()
    FILELIST.append(file.getfilelist)
    MUTEX.release()


def fucconvertfile(filepath):
    '转换文件'
    file = FileConvert(filepath)
    file.convert()

def funccountfile(filepath):
    '计算空车数量'
    file = FileCount(filepath)
    file.run()
    MUTEX.acquire()
    FILERESULT = file.getresult()
    MUTEX.release()

def countresult(directory):
    "输出计算后的文件"
    directory = directory+'_count'
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
