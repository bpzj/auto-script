# -*- coding: utf-8 -*-
""" 适用于部署 jdk maven项目 """
import json
import os
import re
import time
import sys
import paramiko

java_exe = u"\"D:\\Program Files (Dev)\\Java\\jdk1.8.0_201\\bin\\java.exe\""
mvn_exe = u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\""
# mvn_exe = r'''"D:\Program Files (Dev)\Maven\apache-maven-3.5.4\bin\mvn.cmd"''' 不好使
current = os.path.dirname(os.path.abspath(__file__))


def local_package(project):
    p = json.load(open(os.path.join(current, 'project.json'), encoding='utf-8'))
    proj = p.get(project)
    os.chdir(proj.get('package_command_path'))
    # os.system(u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\" package -Dmaven.test.skip=true")
    os.system(proj.get('package_command'))


def connect(conf: dict) -> paramiko.SSHClient:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=conf.get('host'), port=conf.get('port'),
                username=conf.get('username'), password=conf.get('password'))
    return ssh


def upload_file(ssh: paramiko.SSHClient, config: dict) -> paramiko.SFTPClient:
    f = ssh.open_sftp()
    # sftp 的 put命令，需要在 remotepath 中，指定文件的名字
    # f.put(r'D:\Python.zip', r'/10.130.218.69 sftp (10.130.218.69)/nginx/home/nginx/webapps/Python.zip')
    f.put(config.get('local_file_path'), config.get('remote_file_path'))
    return f


def exe_deploy_command(chan: paramiko.Channel, config: dict):
    if config.get('deploy_cmd_path'):
        send_and_result(chan, 'cd ' + config.get('deploy_cmd_path'))
    send_and_result(chan, config.get('deploy_cmd'))


def deploy(conf: str):
    paramiko.util.log_to_file('./log.log')
    config = json.load(open(os.path.join(current, 'deploy_conf.json'), encoding='utf-8')).get(conf)
    ssh = connect(config)  # 连接远程
    upload_file(ssh, config)
    # 建立交互式shell连接
    chan = ssh.invoke_shell()
    chan.settimeout(10)
    out_info = read_out(chan)
    if "select group" in out_info:
        if not select_group(chan, config, out_info):
            exit()

    exe_deploy_command(chan, config)


def select_group(chan: paramiko.Channel, config: dict, out_info: str):
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
    read_out(chan)
    return True


def send_and_result(chan, msg: str):
    chan.send(msg + '\n')
    read_out(chan)


def read_out(chan) -> str:
    out = ''
    while not chan.recv_ready():
        time.sleep(1)
    while chan.recv_ready():
        data = chan.recv(102400).decode('utf-8')
        out = out + data
        sys.stdout.write(data)
        time.sleep(1)
    return out


if __name__ == '__main__':
    # local_package('demo')  # 本地打包项目
    deploy('virtual-box')
