import os
import sys
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, wait
# from FileOper import FileOper

def main(argv=None):
    """
    input fie path
    """
    if argv is None:
        print("请输入正确的文件路径")
        return
    
    path = argv[1]
    if os.path.isdir(path) != True:
        print("请输入正确的文件夹路径.")
        return

    #获取该路径下的所有以.csv结尾的文件
    csvfiles = [os.path.join(r, file) for r, d, files in os.walk(
        path) for file in files if file.endswith(".csv")]
    cpucount = cpu_count()

    #引入线程池进行多线程操作
    executor = ThreadPoolExecutor(cpucount)
    futures = []
    for csv in csvfiles:
        futures.append(executor.submit(funcprocess, csv))
    wait(futures)

def funcprocess(filepath):
    '生成文件操作对象，并处理'
    file = FileOper(filepath)
    file.processfile(filepath)

if __name__ == "__main__":
    sys.exit(main())
