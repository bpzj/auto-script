""" 适用于部署 jdk maven项目 """
import time
import sys


def deploy():
    import paramiko
    paramiko.util.log_to_file('./test')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname='10.135.52.138', port=22, username='cuiyang06', password='')
    # 建立交互式shell连接
    chan = ssh.invoke_shell()
    chan.settimeout(10)

    f = chan.transport.open_sftp_client()
    # sftp 的 put命令，需要在 remotepath 中，指定文件的名字
    f.put(r"D:\Python.zip", r"/10.130.218.69 sftp (10.130.218.69)/nginx/home/nginx/webapps/Python.zip")

    # read_out(chan)
    # send_and_result(chan, "5")
    # send_and_result(chan, "cd ./webapps")
    # send_and_result(chan, "bash ./restart.sh")
    # send_and_result(chan, "4")
    # send_and_result(chan, "y")


def select_group(chan, group):
    chan.send(group + "\n")
    read_out(chan)


def send_and_result(chan, msg: str):
    chan.send(msg + "\n")
    read_out(chan)


def read_out(chan):
    while not chan.recv_ready():
        time.sleep(1)
    while chan.recv_ready():
        data = chan.recv(1024).decode("utf-8")
        sys.stdout.write(data)
        time.sleep(1)


if __name__ == '__main__':
    deploy()
    # test()
