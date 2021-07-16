#!/bin/bash

if [ -z `command -v sshd` ] ; then 
    pkg install openssh
fi

rm ~/.ssh/authorized_keys
curl "https://raw.githubusercontent.com/bpzj/script/master/ssh/id_rsa.pub" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh 

# 4. 修改 /etc/ssh/sshd_config 配置文件
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' $PREFIX/etc/ssh/sshd_config


