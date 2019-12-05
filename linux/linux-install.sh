#!/bin/bash

# 全局变量
input="N"
# 通用校验输入的方法
function checkInput() {
    while true; do
        read -t 60 -p "$1" input
        case $input in
            [YyNn]* ) break;;
            * ) echo "Please enter Y/y/N/n .";;
        esac
    done
}

# Linux下安装Git服务器
# 1. 首先登陆root用户
if [ `whoami` == "root" ] ; then
    echo "root has login"
else
    echo "login root user, please input password"
    su root
fi

ins_li=("apt" "yum" "brew")
ins_pre=""


# = 与 == 在 [ ] 中表示判断(字符串比较)时是等价的
# 获取当前系统
OS=`uname -a`

if [[ "$OS" =~ "Ubuntu" ]]; then
	echo "system is Ubuntu"
#	apt-get update
	ins_pre=${ins_li[0]}
elif [[ "$OS" =~ "Darwin" ]]; then
	echo "system is macOS "
	ins_pre=${ins_li[3]}
else
	echo "system unsupport, exit."
	exit 0
fi

# 3. 安装git
result=`command -v git | grep -w "git" -c`
# result 等于0 表示没有找到git 命令，需要安装git，不同系统安装命令不一样
if [ $result -le 0 ]; then
    echo "Install git"
    "$ins_pre" install git
else
    echo "Git installed"
fi

# 是否安装 open-jdk 8
checkInput "Do you want to install open jdk 8: ";
#if [ "$input" == "Y" -o "$input" = "y" ] ; then
  "$ins_pre" install openjdk-8-jdk-headless
#fi
