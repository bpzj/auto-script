# 1. 首先登陆root用户
if [ `whoami` == "root" ] ; then
    echo "root has login"
else
    echo "login root user, please input password"
    su root
fi

# 2. 根据传入参数, 创建用户
USER_NAME='bpzj'
USER_COUNT=`cat /etc/passwd | grep "^$USER_COUNT:" -c`

if [ $USER_COUNT -ne 1 ]
    then
		useradd $USER_NAME
		echo "4260" | passwd --stdin $USER_NAME
    else
		echo 'user exits'
fi
