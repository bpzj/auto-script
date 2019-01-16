#!/bin/bash


path=''$HOME'/Downloads/package'
mkdir -p "$path"

app=`ls "$path" | grep -i "mongodb-osx.tgz"`
# -z 判断长度是否为零，为零 则为真
if [ -z "$app" ] ; then
    curl -o ''$path'/mongodb-osx.tgz' https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-4.0.5.tgz
fi

# 解压缩文件，如果已经有文件夹了，就不解压
mongodbDir=`cd "$path" && find * -maxdepth 0 -type d | grep "mongodb"`
echo $mongodbDir
if [ -z "$mongodbDir" ] ; then
    tar -xvzf ''$path'/'$app'' -C "$path"
    # 解压后，再次获取解压后的文件夹名称
    mongodbDir=`cd "$path" && find * -maxdepth 0 -type d | grep "mongodb"`
fi

if [ ! $mongodbDir == "mongodb" ] ; then
    # 重命名解压后的文件夹 为 mongodb
    echo 'mongodb文件夹名称为'$mongodbDir',准备更改'
    mv ''$path'/'$mongodbDir'' ''$path'/mongodb'
fi