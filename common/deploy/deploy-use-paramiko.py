""" 适用于部署 jdk maven项目 """
import json
import os
import re
import time
import sys
import paramiko

java_exe = u"\"D:\\Program Files (Dev)\\Java\\jdk1.8.0_201\\bin\\java.exe\""
mvn_exe = r'''"D:\Program Files (Dev)\Maven\apache-maven-3.5.4\bin\mvn.cmd"'''
current = os.path.dirname(os.path.abspath(__file__))

# mvn_exe = u"\"D:\\Program Files (Dev)\\Maven\\apache-maven-3.6.0\\bin\\mvn.cmd\""


def connect(dest) -> paramiko.SSHClient:
    j = json.load(open(os.path.join(current, 'deploy_machine_mine.json')))
    m = j.get(dest)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=m.get('host'), port=m.get('port'), username=m.get('username'), password=m.get('password'))
    return ssh


def local_package(project):
    p = json.load(open(os.path.join(current, 'project.json')))
    proj = p.get(project)
    os.chdir(proj.get('package_command_path'))
    # os.system(mvn_exe + " package -Dmaven.test.skip=true")


def upload_file(ssh: paramiko.SSHClient, project: str) -> paramiko.SFTPClient:
    p = json.load(open(os.path.join(current, 'project.json')))
    proj = p.get(project)
    f = ssh.open_sftp()
    # sftp 的 put命令，需要在 remotepath 中，指定文件的名字
    # f.put(r'D:\Python.zip', r'/10.130.218.69 sftp (10.130.218.69)/nginx/home/nginx/webapps/Python.zip')
    f.put(proj.get('local_file_path'), proj.get('remote_file_path'))
    return f


def deploy(dest, project):
    paramiko.util.log_to_file('./log.log')
    local_package(project)  # 本地打包项目
    ssh = connect(dest)  # 连接远程
    # upload_file(ssh, project)

    # 建立交互式shell连接
    chan = ssh.invoke_shell()
    chan.settimeout(10)
    read_out(chan)
    # re.match()
    # if read_out(chan)
    # send_and_result(chan, '5')
    # send_and_result(chan, 'cd ./webapps')
    # send_and_result(chan, 'bash ./restart-java-project.sh')
    # send_and_result(chan, '4')
    # send_and_result(chan, 'y')


def select_group(chan, group):
    chan.send(group + '\n')
    read_out(chan)


def send_and_result(chan, msg: str):
    chan.send(msg + '\n')
    read_out(chan)


def read_out(chan) -> str:
    out = ''
    while not chan.recv_ready():
        time.sleep(1)
    while chan.recv_ready():
        data = chan.recv(1024).decode('utf-8')
        out = out + data
        sys.stdout.write(data)
        time.sleep(1)
    return out


if __name__ == '__main__':
    deploy('aliyun', 'demo')
