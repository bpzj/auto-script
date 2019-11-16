""" 适用于部署 jdk maven项目 """

from paramiko import SSHClient
from paramiko import AutoAddPolicy
import json
import os


def deploy(project: str):
    j = json.load(open(os.path.join(os.path.abspath("."), "deploy.json")))

    print(j.get(project))


if __name__ == '__main__':
    deploy("demo")
