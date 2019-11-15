""" 适用于部署 jdk maven项目 """

from paramiko import SSHClient
from paramiko import AutoAddPolicy


def deploy():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    client.connect(hostname='10.135.52.138', port=22, username='cuiyang06', password='Pass123456')
    stdin, stdout, stderr = client.exec_command('ls -l')
    print(stdin, stdout, stderr)
    client.close()
    pass


if __name__ == '__main__':
    deploy()
