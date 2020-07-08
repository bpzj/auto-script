#!/usr/bin/env bash
# 通过检查本地文件是否变动, 来重启进程
# TODO 增加项目参数, 适配不同的项目
jarFile="/home/nginx/webapps/ypgl-1.0.0.jar"
jarFile="/root/1.txt"

# 上一次文件状态
last=`stat $jarFile |grep Modify`
while [[ "" == "" ]]; do
  update=`stat $jarFile |grep Modify`
  if [[ "$update" == "$last" ]]; then
    echo "file is old"
    sleep 1
  else
    echo "file is updating"
    # 判断文件是否update完成, 如果文件update到一半执行命令, 会报错
    while [[ "" == "" ]]; do
      if [[ "$update" == "$last" ]]; then
        echo "update file finish"
        process=`ps -ef|grep "java -jar"|grep ypgl-1.0.0.jar |grep -v grep|awk '{print $2}'`
        if [ -n "$process" ] ; then
          kill -9 $process
        fi
        cd /home/nginx/webapps && nohup java -jar ypgl-1.0.0.jar --spring.profiles.active=int > ypgl.log &
        # 把更新后的赋值给 last
        last=$update

        # 跳出循环
        break
      else
        last=$update
        sleep 1
        update=`stat $jarFile |grep Modify`
      fi
    done
  fi

done

