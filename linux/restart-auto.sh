#!/usr/bin/env bash
file="/root/webapps/ypgl-1.0.0.jar"
last=`stat $file |grep Modify`
while [[ "" == "" ]]; do
  modify=`stat $file |grep Modify`
  if [[ "$modify" == "$last" ]]; then
    echo "same"
  else
    echo "not same"
    sleep 20
    process=`ps -ef|grep "java -jar"|grep "$jarFile" |grep -v grep|awk '{print $2}'`
    if [ -n "$process" ] ; then
      kill -9 $process
    fi
    cd /root/webapps && nohup java -jar ypgl-1.0.0.jar --spring.profiles.active=test > ypgl.log &
    last=$modify
  fi

  sleep 1
done
