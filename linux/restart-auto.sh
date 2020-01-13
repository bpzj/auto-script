#!/usr/bin/env bash
jarFile="/home/nginx/webapps/ypgl-1.0.0.jar"
last=""
while [[ "" == "" ]]; do
  modify=`stat $jarFile |grep Modify`
  if [[ "$modify" == "$last" ]]; then
    echo "same"
  else
    echo "not same"
    sleep 30
    process=`ps -ef|grep "java -jar"|grep ypgl-1.0.0.jar |grep -v grep|awk '{print $2}'`
    if [ -n "$process" ] ; then
      kill -9 $process
    fi
    cd /home/nginx/webapps && nohup java -jar ypgl-1.0.0.jar --spring.profiles.active=int > ypgl.log &
    last=$modify
  fi

  sleep 1
done
