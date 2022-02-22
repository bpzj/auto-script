import os


def get_dir():

    # 获取 本python文件的 在哪个问价夹, 不论调用本方法的是哪个文件
    path1 = os.path.dirname(__file__)
    print(path1)

    # os.path.realpath(os.path.curdir) 获取的是
    #   调用此方法的文件  的路径
    path2 = os.path.realpath(os.path.curdir)
    print(path2)

    # 获取一个路径的父路径
    print(os.path.dirname(path1))
    pass


if __name__ == '__main__':
    get_dir()
