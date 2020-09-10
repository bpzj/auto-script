#!/bin/bash

count=`find . -maxdepth 1 -name '*.jar'|wc -l`
if [ "$count" -le 0 ] ; then
    echo "脚本所在目录下没有jar文件"
    exit 0
fi

jarFile=''
if [[ -f $1 && $1 =~ '.jar' ]] ; then
    jarFile=$1
else
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
    while [ $num -gt $count ]
    do
        echo "不存在数字对应的项目"
        checkNum "请输入要启动的项目: "
    done
    jarFile=`ls|grep .jar$|sed -n "$num"p`
fi



################  准备要执行的参数 ################
process=`ps -ef|grep "java.*.jar"|grep "$jarFile" |grep -v grep|grep -v .sh|awk '{print $2}'`
log=${jarFile/.jar/.log}
hprof=${jarFile/.jar/.hprof}
if [ -n "$process" ] ; then
    # todo 存在原来的进程 取原来的参数
#    args=`ps -ef|grep "java"|grep "$jarFile"|grep -v grep|sed -r 's/.*java {1,}-jar {1,}.*?.jar {1,}//'`
    if [[ -z "$1" ]] ; then
        echo -e "\033[31m支持使用 bash ""$0"" ""$jarFile"" 来重启应用\033[0m"
    fi
    args=`ps -ef|grep "java.*.jar"|grep "$jarFile"|grep -v grep|grep -v .sh|sed -r 's/.*java //'`
else
    # 如果不存在原来的进程，说明是新启动，可能需要加额外参数
    args=""
    read -t 120 -p "输入想要启动的yml配置文件: " active
    read -t 120 -p "远程调试端口(不开启直接回车): " debug
    read -t 120 -p "开启溢出转存(不开启直接回车): " dump
    read -t 120 -p "请输入JVM虚拟机参数         : " jvm
    read -t 120 -p "请输入应用程序参数          : " other
     if [ -n "$jvm" ]; then
        args="$args $jvm"
    fi
    if [ -n "$debug" ]; then
        args="$args -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=$debug"
    fi
    if [ -n "$dump" ]; then
        args="$args -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=$hprof"
    fi
    args="$args -jar $jarFile"
    if [ -n "$active" ]; then
        args="$args --spring.profiles.active=$active"
    fi
    if [ -n "$other" ]; then
        args="$args $other"
    fi
fi



################  输出要执行的参数 ################
echo "即将执行:"
if [ -n "$process" ] ; then
    echo "    kill -9 $process"
fi
    echo "    nohup java $args > $log 2>&1 &"



################  确认执行命令  ################
input=''
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

# 循环遍历参数
for arg in $*
  do
     if [ "$arg" == '-y' ]; then
        input='y'
     fi
  done

if [[ -z $input ]]; then
    checkInput "确认(Enter=Y/Y/y/N/n)："
fi
if [ $input == "N" -o $input = "n" ] ; then
    exit 0
fi


################  执行命令  ################
if [ -n "$process" ] ; then
  kill -9 $process
fi
  nohup java $args > $log 2>&1 &

tail -f $log

