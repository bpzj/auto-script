# 通用校验输入的方法
function confirmSoftware() {
    while true; do
        echo -e -n "是否要 \e[1;31m$1\e[m，默认[$2] :" 
        read -t 60 input
        # 什么都不输入，直接回车，按 N 处理
	if [ -z $input ] ; then 
        if [ $2 == "Y" ]; then 
            return 1; 
        else 
            return 0;
        fi; 
    fi
        case $input in
            [Yy] ) return 1;;
            [Nn] ) return 0;;
            * ) echo "只能输入 [Y/y/N/n].";;
        esac
    done
}