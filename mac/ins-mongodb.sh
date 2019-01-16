#!/bin/bash


path=''$HOME'/Downloads/package'

app=`ls "$path" | grep -i "mongodb-osx.tgz"`
# -z 判断长度是否为零，为零 则为真
if [ -z "$app" ] ; then
    curl -o ''$path'/mongodb-osx.tgz' https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-4.0.5.tgz
fi
mkdir -p "$path"
