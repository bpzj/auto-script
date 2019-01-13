#!/bin/bash

# 获取当前系统
OS=`uname -s`
if [ $OS == "Darwin" ];then
	echo "系统为 macOS "
elif [ $OS == "Linux" ];then
	echo "系统为 Linux"
else
	echo "系统为: $OS, 暂不支持, 退出运行."
fi

# todo distribution 发行版
dist=`uname -a`


# 如果是linux系统登录root用户
if [ $OS == "Linux" ] ; then
    if [ `whoami` == "root" ] ; then
        echo "root has login"
    else
        echo "login root user, please input password"
        su root
    fi
fi




