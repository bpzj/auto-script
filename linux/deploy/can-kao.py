import sys

import paramiko


def test():
    paramiko.util.log_to_file('./test')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    # todo
    ssh.connect(hostname='10.135.52.138', port=22, username='', password='')
    channel = ssh.invoke_shell()
    channel.settimeout(10)

    buff = ''
    resp = ''
    channel.send('ssh cuiyang06' + '@10.135.52.138' + '\n')  # 发送ssh root@192.168.1.20

    while not str(buff).__contains__("Select group:"):  # 是否以字符串 's password 结尾
        try:
            resp = channel.recv(256)
        except Exception as e:
            print('Error info:%s connection time.' % (str(e)))
            channel.close()
            ssh.close()
            sys.exit()
        buff = buff + str(resp)
        print(buff)
        if not buff.find('yes/no') == -1:  # 模拟ssh登陆是输入yes
            channel.send('yes\n')
        buff = ''

    channel.send('1\n')  # 发送密码

    buff = ''
    while not buff.endswith('# '):
        resp = channel.recv(9999)
        if not resp.find("passinfo") == -1:
            print('Error info: Authentication failed.')
            channel.close()
            ssh.close()
            sys.exit()
        buff += resp

    channel.send('ping www.qq.com -c 4\n')
    buff = ''
    try:
        while buff.find('# ') == -1:
            resp = channel.recv(9999)
            buff += resp
    except Exception as e:
        print("error info:" + str(e))

    print(buff)
    channel.close()
    ssh.close()

