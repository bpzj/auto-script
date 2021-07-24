import os

path = 'C:\\Users\\Administrator\\Desktop\\all-kinds-of-books\\哲学\\毛泽东著作\\毛泽东思想万岁\\5'

for root, dirs, files in os.walk(path):
    for file in files:
        print('\\input{' + file + '}')
