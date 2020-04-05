
scp C:\Users\bpzj\Desktop\all-code\script\linux\inotify.sh root@192.168.56.104:/root && ssh root@192.168.56.104 "bash /root/inotify.sh"

scp C:\Users\bpzj\Desktop\all-code\script\linux\linux-install.sh root@192.168.56.104:/root && ssh root@192.168.56.104 "bash /root/linux-install.sh"

## 在 Windows系统 中调试 Linux 脚本:
思路: 上传shell脚本文件到一个真实的linux环境, 本地ssh执行远程脚本
- 准备一个 linux 环境 (推荐虚拟机)
- windows 中安装 openssh, 并配置root 使用秘钥免密码登录上面的linux环境
- 使用下面的命令运行
```shell script
# 执行远程脚本
ssh root@192.168.56.104 "bash /root/inotify.sh"

# 上传并执行脚本:
scp linux\inotify.sh root@192.168.56.104:/root && ssh root@192.168.56.104 "bash /root/inotify.sh"
```
