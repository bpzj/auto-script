import os
import shutil


# 删除 符合规则的 文件夹


# 遍历当前文件夹下第一层文件
def traversal_first_layer():
    """
    在本 Python 脚本所在的文件夹遍历，只遍历第一层
    """
    for root, dirs, files in os.walk('./'):
        print(root)
        for dir_name in dirs:
            print(dirs)
            print(dir_name)
            # print(files)
            # if dir_name.endswith(".idea"):
            #     # os.remove(os.path.join(root, dir_name))
            #     shutil.rmtree(os.path.join(root, dir_name))
            # elif dir_name.endswith("target"):
            #     shutil.rmtree(os.path.join(root, dir_name))
            # elif dir_name.endswith("log"):
            #     shutil.rmtree(os.path.join(root, dir_name))
            # elif dir_name.endswith("logs"):
            #     shutil.rmtree(os.path.join(root, dir_name))




