import os

path = 'C:\\Users\\Administrator\\Desktop\\all-kinds-of-books\\哲学\\毛泽东著作\\毛泽东思想万岁\\5'

for root, dirs, files in os.walk(path):
    for file in files:
        print('\\input{' + file + '}')
        # num = int(file[2:5])
        # if num < 400 and num > 150:
            # new = file[:2]+ "{0:03d}".format(num-10)+file[5:]
            # os.renames(os.path.join(path, file), os.path.join(path, new))
            # print('\\input{' + file + '}')
