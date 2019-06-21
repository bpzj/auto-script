# -*- coding=utf-8 -*-

import subprocess
import os

java_exe = u"\"D:\\Program Files (Dev)\\Java\\jdk1.8.0_201\\bin\\java.exe\""

# D:\Program Files (Dev)\Maven\apache-maven-3.6.0\bin\mvn.cmd
mvn_exe = u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\""

project = u""

print(u'测试开始')
# os.system('chcp 65001')
os.system(mvn_exe + " package")
# subprocess.Popen('dir', shell=True)
# subprocess.Popen(java_exe, shell=True)
# subprocess.Popen(mvn_exe + " package", shell=True)

# subprocess.Popen('ping 192.168.1.1', shell=True)


