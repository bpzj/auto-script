# 以管理员身份运行powershell

#启用WSL
# Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

#创建目录
# New-Item D:\wsl -ItemType Directory
# Set-Location D:\wsl
Set-Location D:\
    #下载安装程序，这个过程比较慢，要多等一段时间
# Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1604 -OutFile ubuntu.appx -UseBasicParsing
    
    # Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804-arm -OutFile ubuntu.appx -UseBasicParsing
    #Invoke-WebRequest -Uri https://aka.ms/wsl-debian-gnulinux -OutFile debian.appx -UseBasicParsing

# Rename-Item .\ubuntu.appx ubuntu.zip
# Expand-Archive .\ubuntu.zip -Verbose
