import json
import os
import time
from stat import S_ISDIR
import paramiko

current = os.path.dirname(os.path.abspath(__file__))


def connect(conf: dict) -> paramiko.SFTPClient:
    paramiko.util.log_to_file('./sync.log')
    print('准备连接远程地址')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=conf.get('host'), port=conf.get('port'),
                username=conf.get('username'), password=conf.get('password'))
    # config = json.load(open(os.path.join(current, 'deploy_conf.json'), encoding='utf-8')).get(conf)
    sftp = ssh.open_sftp()
    return sftp


def files_of_dir(f: paramiko.SFTPClient, remote_dir) -> list:
    all_file = []
    file_list = f.listdir_attr(remote_dir)
    for file in file_list:
        file_name = remote_dir + "/" + file.filename
        if S_ISDIR(file.st_mode):
            all_file.extend(files_of_dir(f, file_name))
        else:
            all_file.append(file_name)
    return all_file


def download_file(sftp: paramiko.SFTPClient, sync_remote=r'/root/sync', local_path='D:\\sync\\'):
    remote_all = files_of_dir(sftp, sync_remote)
    for file in remote_all:
        name = str(file).replace(sync_remote, '')
        name = name[1:] if name.startswith("/") else name
        local = os.path.join(local_path, name)
        abs_path = os.path.abspath(os.path.dirname(local))
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        print("downloading: ", local)
        sftp.get(file, local)


def upload_file(sftp, sync_remote, local_path):
    pass


def sync_dir(config):
    sftp = connect(config)
    sync_remote = r'/root/sync'
    sync_remote = r'/10.130.218.69 sftp (10.130.218.69)/nginx/home/nginx/sync'
    remote_old = sftp.stat(sync_remote)
    local_path = r'C:\Users\bpzj\Desktop\all-code\work'
    local_old = os.stat(local_path)
    while True:
        # st_mtime modification - 最近修改时间
        if not sftp.stat(sync_remote).st_mtime == remote_old.st_mtime:
            download_file(sftp, sync_remote, local_path)
            remote_old = sftp.stat(sync_remote)
            local_old = os.stat(local_path)
        elif os.stat(local_path).st_mtime == local_old.st_mtime:
            upload_file(sftp, sync_remote, local_path)
            local_old = os.stat(local_path)
            remote_old = sftp.stat(sync_remote)
        else:
            print("no change")
            time.sleep(5)


if __name__ == '__main__':
    conf = {'host': '192.168.56.104', 'port': 22, 'username': 'root', 'password': '4260'}
    conf = {'host': '10.135.52.138', 'port': 22, 'username': 'itw_shenzl', 'password': 'Pass654321'}
    sync_dir(conf)
