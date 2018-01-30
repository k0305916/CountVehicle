import os
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


def main(path):
    """
    input fie path
    """
    if os.path.isdir(path) != True:
        print("请输入正确的文件夹路径.")
        return

    #获取该路径下的所有以.csv结尾的文件
    os.walk(path)
    csvfiles = [os.path.join(r, file) for r, d, files in os.walk(
        path) for file in files if file.endswith(".csv")]
    cpucount = cpu_count()

    #引入线程池进行多线程操作
    executor = ThreadPoolExecutor(cpucount)
    for csv in csvfiles:
        executor.submit(processfile, csv)
    executor


def processfile(filepath):
    """
    处理文件
    """
    f_read = open(filepath)


main("E:\\Business\\Program\\Python\\CountVehicle\\data")
