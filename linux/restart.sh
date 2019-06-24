#!/bin/bash

input="0"
path=`pwd | cat`

echo $path
echo "重启 followup   ：2"
echo "重启 cdi        ：3"
echo "重启 kb         ：4"
echo "重启 prescription   ：5"

echo ""
echo "重启 cdi-engine     ：6"
echo "重启 outward        ：7"

echo ""
echo "重启 sys    ：8"
echo "重启 his    ：9"

yml=`ps -ef | grep java |grep -v grep|awk '{print $11}'|awk -F"=" 'NR==1{print $2}'`

checkInput "请输入要重启的项目: "
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





#kill -9 $(ps -ef | grep life-main-service|grep -v grep|awk '{print $2}')
#nohup java -Xmx1024m -XX:MaxPermSize=128M -jar /u02/tomcat/life/les/life-main-service.jar --server.port=8080 --spring.application.name=SC509-LESUPPORT --spring.profiles.active=dev -Dfile.encoding=UTF-8 > /u02/tomcat/life/les/nohup.out &
#nohup java -jar /u02/tomcat/life/les/life-main-service.jar --server.port=8080 --spring.profiles.active=dev > /u02/tomcat/life/les/nohup.out &
#tail -f /u02/tomcat/life/les/nohup.out
