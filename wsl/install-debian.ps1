# 以管理员身份运行powershell

#启用WSL
# Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

#创建目录
# New-Item D:\wsl -ItemType Directory
# Set-Location D:\wsl
$path='D:\'
Set-Location $path
    #下载安装程序，这个过程比较慢，要多等一段时间
# Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1604 -OutFile ubuntu.appx -UseBasicParsing
    
    # Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804-arm -OutFile ubuntu.appx -UseBasicParsing
    #Invoke-WebRequest -Uri https://aka.ms/wsl-debian-gnulinux -OutFile debian.appx -UseBasicParsing

# 解压appx文件
# Rename-Item .\ubuntu.appx ubuntu.zip
# -Verbose 显示命令运行的过程，这里是显示解压过程
Expand-Archive -Path .\ubuntu.zip -DestinationPath .\ubuntu-tar -Force -Verbose

# 获取tar.gz 安装包路径
$tar=$path.TrimEnd('\') + '\ubuntu-tar\install.tar.gz'
echo $tar

# 安装wsl
&"D:\Program Files (Dev)\LxRunOffline\LxRunOffline.exe"  i -n ubuntu -d 'D:\ubuntu' -f $tar
pause