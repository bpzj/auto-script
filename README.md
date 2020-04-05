# auto-script 自动化脚本

执行 mac 或 linux 安装软件脚本
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/bpzj/auto-install/master/auto-install.sh)" 
```

执行 Android termux 安装脚本
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/bpzj/auto-install/master/android-install.sh)" 
```

## common
[监视git目录, 有新提交上传指定文件到远程服务器](./common/file_upload_paramiko.py)

[执行java maven打包命令](./common/java_maven_pkg.py)

[python获得windows系统中命令行的输出](./common/get_cmd_out.py)


## Linux
[Linux安装后初始化, 安装git, jdk, 等等](./linux/linux-install.sh)

[创建一个Git服务器](./linux/ins-git-server.sh)

[自动重启java项目](./linux/restart-java-project.sh)

[配置ssh通过秘钥访问](./linux/ssh-over-RSA.sh)

[执行远程Linux机器上的shell脚本](./linux/执行远程Linux机器上的shell脚本.md)


## windows
[使用OneDrive同步任意位置的文件夹](./windows/onedrive-any-where.ps1)

[开启热点](./windows/open_hotspot.ps1)

[自动配置环境变量](./windows/set-path.ps1)

[删除不必要的服务](./windows/删除无用服务.ps1)

[安装Linux子系统](./windows/wsl1/install-debian.ps1)

