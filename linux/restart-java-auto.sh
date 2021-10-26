#!/usr/bin/env bash
# 通过检查本地文件是否变动, 来重启进程
# 后台运行本命令
#  nohup bash ./restart-auto.sh  xxx.jar --spring.profiles.active=uat > restart.log &
#  $# 为参数个数, $1 为第一个参数
# todo 考虑如何更方便的后台运行本脚本
if [ $# -eq 0 ] ; then
  echo "没有参数, 请输入要重启的 jar 文件"
  exit 0
fi
if [ ! -f $1 ] ; then
  echo "文件不存在"
  exit 0
fi
# ${string##*chars}	从 string 字符串最后一次出现 *chars 的位置开始，截取 *chars 右边的所有字符。
if [[ ! ${1##*.} == "jar" ]] ; then
  echo "文件不是jar文件"
  exit 0
fi

log=`echo $1 | sed 's/.jar$/.log/g'`
# 上一次文件状态
last=`stat $1 |grep Modify`
while [[ 1 ]]; do
  update=`stat $1 |grep Modify`
  if [[ "$update" == "$last" ]]; then
#    echo "file is old"
    sleep 10
  else
    echo "file is updating"
    # 判断文件是否 update完成, 如果文件update到一半执行命令, 会报错
    while [[ 1 ]]; do
      if [[ "$update" == "$last" ]]; then
        echo `date "+%m-%d %H:%M:%S"`" update file finish"

        process=`ps -ef|grep "java -jar"|grep $1|grep -v grep|awk '{print $2}'`
        if [ -n "$process" ] ; then
          kill -9 $process
        fi

        nohup java -jar $1 $2 > $log 2>&1 &
        # 把更新后的赋值给 last
        last=$update

        # 跳出循环
        break
      else
        last=$update
        sleep 1
        update=`stat $1 |grep Modify`
      fi
    done
  fi

done

