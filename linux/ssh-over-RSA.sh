#!/bin/bash

# 4. 修改 /etc/ssh/sshd_config 配置文件
file="/etc/ssh/sshd_config"
line1=`grep -n "^.*AuthorizedKeysFile.*authorized_keys.*" $file | cut -d ":" -f 1`
echo $line1
    # 如果不存在此行，就在文件最后加一行，如果存在此行，直接替换
    # -z 判断长度是否为零，长度为0，表示没有这一行
if [ -z "$line1" ]; then
    echo "AuthorizedKeysFile .ssh/authorized_keys" | sudo tee -a $file
else
    sed -i ''$line1'c\AuthorizedKeysFile .ssh/authorized_keys' $file
fi
line1=`grep -n "^.*AuthorizedKeysFile.*authorized_keys.*" $file | cut -d ":" -f 1`

    # 如果不存在此行，就在上面的那行前边插入
line2=`grep -n "^.*PubkeyAuthentication.*yes.*" $file | cut -d ":" -f 1`
echo $line2
if [ -z "$line2" ]; then
    sed -i ''$line1'i\PubkeyAuthentication yes' $file
else
    sed -i ''$line2'c\PubkeyAuthentication yes' $file
fi
line2=`grep -n "^.*PubkeyAuthentication.*yes.*" $file | cut -d ":" -f 1`


    # 如果不匹配，就在上面的那行前边插入
line3=`grep -n "^.*RSAAuthentication.*yes.*" $file | cut -d ":" -f 1`
echo $line3
if [ -z "$line3" ]; then
    sed -i ''$line2'i\RSAAuthentication yes' $file
else
    sed -i ''$line3'c\RSAAuthentication yes' $file
fi
    # 重启sshd服务
sudo service sshd restart



