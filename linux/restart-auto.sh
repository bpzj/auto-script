#!/usr/bin/env bash
# 通过检查本地文件是否变动, 来重启进程
# TODO 增加项目参数, 适配不同的项目
#  $# 为参数个数, $1 为第一个参数
if [ $# -eq 0 ] ; then
  echo "没有参数, 请输入要重启的 jar 文件"
  exit 0
fi
if [ ! -f $1 ] ; then
  echo "文件不存在"
  exit 0
fi
if [[ ! ${1##*.} == "jar" ]] ; then
  echo "文件不是jar文件"
  exit 0
fi

log=`echo $1 | sed 's/.jar$/.log/g'`
# 上一次文件状态
last=`stat $1 |grep Modify`
while [[ "" == "" ]]; do
  update=`stat $1 |grep Modify`
  if [[ "$update" == "$last" ]]; then
#    echo "file is old"
    sleep 10
  else
    echo "file is updating"
    # 判断文件是否update完成, 如果文件update到一半执行命令, 会报错
    while [[ "" == "" ]]; do
      if [[ "$update" == "$last" ]]; then
        echo "update file finish"
        process=`ps -ef|grep "java -jar"|grep $1 |grep -v grep|awk '{print $2}'`
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

