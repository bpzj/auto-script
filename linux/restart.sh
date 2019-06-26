#!/bin/bash

input="0"
path=`pwd | cat`
echo $path

jarFile=`find $path -maxdepth 1 -name '*.jar'`
echo $jarFile


yml=`ps -ef | grep java | grep -v grep | awk -F'active=' '{print $2}' | awk 'NR==1{print $1}'`

if [ $input == "1" ] ; then
    kill -9 $(ps -ef | grep cdm-basic |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-basic-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "2" ] ; then
    kill -9 $(ps -ef | grep cdm-followup |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-followup-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "3" ] ; then
    kill -9 $(ps -ef | grep cdm-cdi |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-cdi-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "4" ] ; then
    kill -9 $(ps -ef | grep cdm-kb |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-kb-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "5" ] ; then
    kill -9 $(ps -ef | grep cdm-prescription |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-prescription-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "6" ] ; then
    kill -9 $(ps -ef | grep cdm-cdi-engine |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-cdi-engine-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "7" ] ; then
    kill -9 $(ps -ef | grep cdm-outward |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-outward-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "8" ] ; then
    kill -9 $(ps -ef | grep cdm-sys |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-sys-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

if [ $input == "9" ] ; then
    kill -9 $(ps -ef | grep cdm-his |grep -v grep|awk '{print $2}')
    nohup java -jar /home/nginx/webapps/cdm-his-1.0.0.jar --spring.profiles.active=$yml > /home/nginx/webapps/nohup.out &
    tail -f /home/nginx/webapps/nohup.out
fi

