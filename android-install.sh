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

# = 与 == 在 [ ] 中表示判断(字符串比较)时是等价的
# 获取当前系统
OS=`uname -s`
if [ $OS == "Darwin" ];then
	echo "系统为 macOS "
elif [ $OS == "Linux" ];then
	echo "系统为 Linux"
else
	echo "系统为: $OS, 暂不支持, 退出运行."
fi

# 判断是不是 Android 发行版
result=`uname -a | grep -w "Android" -c`
if [ $result -le 0 ]; then
    echo "系统不是是Android发行版"
    exit
else
    echo "系统是Android发行版"
    OS="Android"
fi

# 1. 安装git
result=`command -v git | grep -w "git" -c`
# result 等于0 表示没有找到git 命令，需要安装git，不同系统安装命令不一样
if [ $result -le 0 ]; then
    echo "Install git"
    pkg update && pkg upgrade
    pkg install git
else
    echo "Git installed"
fi

# 2. 创建一个 文件夹
shared=''$HOME'/storage/shared'
mkdir -p ''${shared}'/0_file'

# 4. git clone 安装脚本到本地
#path='/Users/lym/Desktop/auto-install'
path=''$HOME'/Downloads/auto-install'
#mkdir -p "$path"
#rm -rf "$path"
#git clone git@github.com:bpzj/auto-install.git "$path"



# 7. 安装zsh, 主题ys


