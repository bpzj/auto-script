import os
import shutil


# 删除 符合规则的 文件夹


# 遍历当前文件夹下第一层文件
def traversal_first_layer():
    """
    在本 Python 脚本所在的文件夹遍历，只遍历第一层
    """
    path = 'H:\\yonyou\\production-order\\scripts-bak\\mysql\\PO\\DML\\930'
    target = 'C:\\Users\\Administrator\\Desktop\\4-22-delete-recover\\930\\'

    for root, dirs, files in os.walk(path):
        print(root)
        for dir_name in files:
            f_path = root + '\\' + dir_name
            with open(f_path,encoding='utf-8') as file:
                for content in file:
                    if 'pub_makebillrule' in content:
                        shutil.copy(f_path, target)
            # print(dirs)
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


if __name__ == '__main__':
    traversal_first_layer()
