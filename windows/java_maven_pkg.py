# -*- coding=utf-8 -*-

import subprocess
import os

java_exe = u"\"D:\\Program Files (Dev)\\Java\\jdk1.8.0_201\\bin\\java.exe\""

# D:\Program Files (Dev)\Maven\apache-maven-3.6.0\bin\mvn.cmd
# 两种写法
# mvn_exe = u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\""
mvn_exe = r'''"D:\Program Files (Dev)\Maven\apache-maven-3.6.0\bin\mvn.cmd"'''

project = u""

print(u'测试开始')
# os.system('chcp 65001')
os.chdir(r'C:\Users\bpzj\Desktop\all-code\java-work-experience')
os.system(mvn_exe + " package -Dmaven.test.skip=true")
# subprocess.Popen('dir', shell=True)
# subprocess.Popen(java_exe, shell=True)
# subprocess.Popen(mvn_exe + " package", shell=True)

# subprocess.Popen('ping 192.168.1.1', shell=True)


