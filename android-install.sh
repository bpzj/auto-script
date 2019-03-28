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

# 2. 创建一个名为 0_file 的文件夹，并建一个软连接
shared=''$HOME'/storage/shared'
cd $shared && mkdir -p '0_file'
cd $HOME && rm -f "0_file" && ln -s "$shared/0_file" "0_file"
# 2.1 创建 Tim 接收文件夹的软连接
cd $HOME && rm -f "tim" && ln -s "$shared/tencent/TIMfile_recv" "tim"

# 4. 安装 python、ipython、tushare、pytdx、Pillow

pkg install clang
pkg install libxml2
pkg install libxml2-dev
pkg install libxml2-util
pkg install libxslt
pkg install libxslt-dev
pip install lxml

pkg install libzmq
apt install libzmq-dev
pip install cython
pip install pyzmq

pip install tushare

pkg install libffi
pkg install libffi-dev
pip install cffi
pkg install openssl
pkg install openssl-dev
pkg install openssl-tool
pip install pytdx

pkg install libjpeg-turbo-dev
pip install Pillow




# 7. 安装zsh, 主题ys


