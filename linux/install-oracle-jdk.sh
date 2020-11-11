#!/bin/bash

# 1. 首先登陆root用户
if [ `whoami` == "root" ] ; then
    echo "root has login"
else
    echo "login root user, please input password"
    su root
fi

tar -zxvf jdk-8u271-linux-x64.tar.gz

mkdir -p /usr/local/jdk
mv jdk1.8.0_271/ /usr/local/jdk/

echo "export JAVA_HOME=/usr/local/jdk/jdk1.8.0_271" >> /etc/profile
echo "export JRE_HOME=\${JAVA_HOME}/jre" >> /etc/profile
echo "export CLASSPATH=.:\${JAVA_HOME}/lib:\${JRE_HOME}/lib" >> /etc/profile
echo "export PATH=\${JAVA_HOME}/bin:\$PATH" >> /etc/profile
source /etc/profile
