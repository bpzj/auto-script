# 以管理员身份运行powershell
# runasadministrator
$myWindowsID = [System.Security.Principal.WindowsIdentity]::GetCurrent();
$myWindowsPrincipal = New-Object System.Security.Principal.WindowsPrincipal($myWindowsID);
$adminRole = [System.Security.Principal.WindowsBuiltInRole]::Administrator;
if ($myWindowsPrincipal.IsInRole($adminRole))
{
    # We are running as an administrator, so change the title and background colour to indicate this
    $Host.UI.RawUI.WindowTitle = $myInvocation.MyCommand.Definition + "(Elevated)";
    $Host.UI.RawUI.BackgroundColor =0;
    Clear-Host;
}
else {
    # We are not running as an administrator, so relaunch as administrator
    # Create a new process object that starts PowerShell
    $newProcess = New-Object System.Diagnostics.ProcessStartInfo "PowerShell";

    # Specify the current script path and name as a parameter with added scope and support for scripts with spaces in it's path
    $newProcess.Arguments = "& '" + $script:MyInvocation.MyCommand.Path + "'"

    # Indicate that the process should be elevated
    $newProcess.Verb = "runas";

    # Start the new process
    [System.Diagnostics.Process]::Start($newProcess);

    # Exit from the current, unelevated, process
    Exit;
}

#启用虚拟机平台：
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
# 启用适用于Linux的Windows子系统
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
# Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

#使 WSL 2 成为你的默认体系结构
wsl --set-default-version 2
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