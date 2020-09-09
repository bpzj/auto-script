# -*- coding: utf-8 -*-
""" 适用于部署 jdk maven项目 """
import json
import os
import time
import sys
import paramiko
from stat import S_ISDIR
import win32file
import win32con
import subprocess

current = os.path.dirname(os.path.abspath(__file__))
project = "virtual-box"
config = json.load(open(os.path.join(current, 'deploy_conf.json'), encoding='utf-8')).get(project)


def maven_package(project_path, mvn_cmd=None):
    """ 打包Maven项目 """
    java_exe = u"\"D:\\Program Files (Dev)\\Java\\jdk1.8.0_201\\bin\\java.exe\""
    mvn_exe = u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\""
    # mvn_exe = r'''"D:\Program Files (Dev)\Maven\apache-maven-3.5.4\bin\mvn.cmd"''' 不好使
    os.chdir(project_path)
    # os.system(u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\" package -Dmaven.test.skip=true")
    if mvn_cmd:
        os.system(mvn_cmd)
    else:
        os.system(mvn_exe + " clean package -Dmaven.test.skip=true")


def connect(conf: dict) -> paramiko.SSHClient:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=conf.get('host'), port=conf.get('port'),
                username=conf.get('username'), password=conf.get('password'), auth_timeout=20)
    return ssh


def upload_file(sftp: paramiko.SFTPClient, local_path, remote_path) -> paramiko.SFTPClient:
    local_all = files_of_dir(local_path)
    for file in local_all:
        real_remote = os.path.join(remote_path, file.replace(os.path.dirname(local_path), '').lstrip('\\')).replace("\\", "/")
        remote_p = os.path.dirname(real_remote)
        # 远程创建文件夹
        try:
            stat = sftp.stat(remote_p)
        except FileNotFoundError:
            sftp.mkdir(remote_p)

        stat = sftp.stat(remote_p)
        if S_ISDIR(stat.st_mode):
            # sftp 的 put命令，需要在 remotepath 中，指定文件的名字
            # f.put(r'D:\Python.zip', r'/10.130.218.69 sftp (10.130.218.69)/nginx/home/nginx/webapps/Python.zip')
            sftp.put(file, real_remote)
    return sftp


def files_of_dir(local_path) -> list:
    """获取本地路径下的所有文件"""
    all_file = []
    if os.path.isfile(local_path):
        all_file.append(local_path)
        return all_file
    all_file = []
    for i, j, k in os.walk(local_path):
        for n in k:
            if os.path.isfile(os.path.join(i, n)):
                all_file.append(os.path.join(i, n))
    return all_file


def deploy(conf: str):
    paramiko.util.log_to_file('./log.log')
    config = json.load(open(os.path.join(current, 'deploy_conf.json'), encoding='utf-8')).get(conf)
    print("开始连接远程服务器: ", config.get('host'))
    ssh = connect(config)  # 连接远程
    print("连接远程服务器成功, 准备上传文件")
    upload_file(ssh.open_sftp(), config.get('remote_path'), config.get('local_path'))

    # print("上传文件结束, 执行启动命令")
    # 建立交互式shell连接
    # chan = ssh.invoke_shell()
    # chan.settimeout(10)
    # select_group_or_not(chan, config)
    # exec_command(chan, config.get("deploy_cmd"))
    ssh.close()
    # chan.close()


def exec_command(chan: paramiko.Channel, commands: list):
    for cmd in commands:
        chan.send(cmd + '\n')
        read_out(chan, wait_time=2)


def select_group_or_not(chan: paramiko.Channel, config: dict):
    out_info = read_out(chan, wait_time=3)
    if "elect group" not in out_info:
        return
    idx = '0'
    group_list = out_info.split("\r\n")
    for ip_addr in group_list:
        if config.get("select_ip") in ip_addr:
            idx = ip_addr[1:ip_addr.index(":")].strip()
            print("select " + idx)
            break
    if idx == '0':
        print("ip 未找到")
        return False
    chan.send(idx + '\n')
    read_out(chan, wait_time=3)
    return True


def read_out(chan: paramiko.Channel, wait_time=1) -> str:
    now = time.time()
    out = ''
    while True:
        while chan.recv_ready():
            data = chan.recv(256).decode('utf-8')
            out = out + data
            sys.stdout.write(data)
        #     and time.time() - now > 3
        while not chan.recv_ready() and time.time() - now > wait_time:
            return out


# 老的函数
# def read_out(chan: paramiko.Channel) -> str:
# while not chan.recv_ready():
#     time.sleep(1)
# while chan.recv_ready():
#     data = chan.recv(102400).decode('utf-8')
#     out = out + data
#     sys.stdout.write(data)
#     time.sleep(1)
# return out


def watch_file(path, func, last_change):
    actions = {
        1: "Created",
        2: "Deleted",
        3: "Updated",
        4: "Renamed from something",
        5: "Renamed to something"
    }
    file_list_directory = 0x0001

    # path_to_watch = r'C:\Users\bpzj\Desktop\all-code\java-grammar\.git'
    print('监视此路径的变化: ', path)
    h_dir = win32file.CreateFile(
        path,
        file_list_directory,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    while True:
        results = win32file.ReadDirectoryChangesW(
            h_dir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None)
        last_change = func(last_change)


def upload_callback(last):
    os.chdir(config.get('git_cmd_path'))
    res = subprocess.Popen('git log -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    commit = res.stdout.readlines()[0]
    if last != commit:
        print("有新提交")
        maven_package(config.get('package_cmd_path'))
        print("开始连接远程服务器: ", config.get('host'))
        ssh = connect(config)
        print('连接成功,开始上传文件')
        upload_file(ssh.open_sftp(), config.get('upload_local_path'), config.get('upload_remote_path'))
        ssh.close()
    return commit


if __name__ == '__main__':
    watch_file(config.get('.git_path'), upload_callback, "start")

    # maven_package(project_path)  # 本地打包项目
    # 部署项目('blj-test')
    # 部署项目('blj-test')
    # filePath = 'C:\\myLearning\\pythonLearning201712\\carComments\\01\\'

    # print(i,j,k)
