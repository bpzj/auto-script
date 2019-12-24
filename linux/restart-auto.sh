#!/usr/bin/env bash
jarFile="/nginx/home/nginx/webapps/ypgl-1.0.0.jar"
last=`stat $jarFile |grep Modify`
while [[ "" == "" ]]; do
  modify=`stat $jarFile |grep Modify`
  if [[ "$modify" == "$last" ]]; then
    echo "same"
  else
    echo "not same"
    sleep 20
    process=`ps -ef|grep "java -jar"|grep "$jarFile" |grep -v grep|awk '{print $2}'`
    if [ -n "$process" ] ; then
      kill -9 $process
    fi
    cd /nginx/home/nginx/webapps && nohup java -jar ypgl-1.0.0.jar --spring.profiles.active=int > ypgl.log &
    last=$modify
  fi

  sleep 1
done
