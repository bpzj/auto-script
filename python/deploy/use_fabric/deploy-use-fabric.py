""" 适用于部署 jdk maven项目 """

from fabric import Connection
from invoke import Responder


def deploy():

    conn = Connection(host='10.135.52.138', port=22, user='cuiyang06')
    conn.connect_kwargs.password = ''
    sudopass = Responder(pattern=r'Select group: ', response='6\n')
    conn.run('ls ', pty=True, watchers=[sudopass])
    conn.derive_shorthand()
    # conn.run("7")
    pass


if __name__ == '__main__':
    deploy()
