#!/bin/bash

app=`ls /Applications | grep -i "iterm"`
# -z 判断长度是否为零，为零 则为真
if [ ! -z "$app" ] ; then
    echo "iterm 已安装"
    exit
fi

# todo 未完成
itermZip=`ls | grep -i "iterm.*zip"`
if [ -z "$itermZip" ]; then
    curl -O https://iterm2.com/downloads/stable/iTerm2-3_2_6.zip
else
    itermZip=`ls | grep -i "iterm.*zip"`
fi

if [ -z "$itermZip" ]; then
    echo "未找到iterm压缩文件,是否下载地址失效?"
else
    unzip $itermZip
fi

