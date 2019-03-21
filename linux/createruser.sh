USER_COUNT=`cat /etc/passwd | grep '^bpzj:' -c`
USER_NAME='bpzj'
if [ $USER_COUNT -ne 1 ]
    then
    useradd $USER_NAME
    echo "4260" | passwd $USER_NAME --stdin
    else
    echo 'user exits'
fi
