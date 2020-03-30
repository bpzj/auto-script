#!/bin/bash

count=`find . -maxdepth 1 -name '*.jar'|wc -l`
if [ "$count" -le 0 ] ; then
    echo "脚本所在目录下没有jar文件"
    exit 0
fi


################  显示出来所有的jar文件  ################
echo "当前路径下的项目:"
for ((i=1;i<=$count;i++))
do
    x=${i}"p"
    name=`ls|grep .jar$|sed -n "$x"`
    echo "    "$i":   "$name
done


################    确定要启动的项目   ################ 
num="0"
# 校验输入的是否为数字
function checkNum() {
    while true; do
        read -t 60 -p "$1" num
        case $num in
            [1-9]|[1-9][0-9]* ) break;;
            * ) echo "请输入数字: 1-"$count;;
        esac
    done
}
echo ""
checkNum "请输入要启动的项目: "
while [ "$num" -gt "$count" ]
do
    echo "不存在数字对应的项目"
    checkNum "请输入要启动的项目: "
done


################  准备要执行的参数 ################
jarFile=`ls|grep .jar$|sed -n "$num"p`
process=`ps -ef|grep "java -jar"|grep "$jarFile" |grep -v grep|awk '{print $2}'`
out=${jarFile/.jar/.out}
if [ -n "$process" ] ; then
    # todo 存在原来的进程 取原来的参数
    active=`ps -ef|grep "$jarFile"|grep -v grep|awk -F'active=' '{print $2}'|awk 'NR==1{print $1}'`
else
    # 如果不存在原来的进程，说明是新启动，可能需要加额外参数
    read -t 60 -p "请输入要启动的profile: " active
    read -t 120 -p "请输入额外参数: " args
fi



################  输出要执行的参数 ################
echo "即将执行:"
if [ -n "$process" ] ; then
    echo "    kill -9 $process"
fi
if [ -z "$active" ] ; then
    echo "    nohup java -jar $jarFile $args > $out &"
else
    echo "    nohup java -jar $jarFile --spring.profiles.active=$active $args > $out &"
fi



################  确认执行命令  ################
input="N"
# 通用校验输入的方法
function checkInput() {
    while true; do
        read -t 60 -p "$1" input
        if [ -z $input ] ; then
            input="Y"
            break;
        fi
        case $input in
            [YyNn]* ) break;;
            * ) echo "Please enter Y/y/N/n .";;
        esac
    done
}
checkInput "确认(Y/N)："
if [ $input == "N" -o $input = "n" ] ; then
    exit 0
fi


if [ -n "$process" ] ; then
    kill -9 $process
fi
################  执行命令  ################
if [ -z "$active" ] ; then
    nohup java -jar $jarFile $args > $out &
else
    nohup java -jar $jarFile --spring.profiles.active=$active $args > $out &
fi

tail -f $out

