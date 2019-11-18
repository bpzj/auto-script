#requires -version 4.0
#requires #-runasadministrator

# Get the ID and security principal of the current user account
$myWindowsID = [System.Security.Principal.WindowsIdentity]::GetCurrent();
$myWindowsPrincipal = New-Object System.Security.Principal.WindowsPrincipal($myWindowsID);

# Get the security principal for the administrator role
$adminRole = [System.Security.Principal.WindowsBuiltInRole]::Administrator;

# Check to see if we are currently running as an administrator
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



#创建环境变量
Function Create-EnvVar
{param([Parameter(Mandatory=$true)] $Name, $Value)
   
    [System.Environment]::SetEnvironmentVariable($Name, $Value, [System.EnvironmentVariableTarget]::Machine)

}

#在现有的环境变量后添加值
Function Append-PATH
{param ($Paths)

    $OldValue = [environment]::GetEnvironmentVariable("Path",[System.EnvironmentVariableTarget]::Machine)
    $flag = 0
    for($i=0; $i -lt $Paths.Length; $i++) {
        $Item = $Paths[$i]
        # 如果要添加的值中含有 %，认为用到了其他环境变量
        if($Item.Contains("%")){
            $Base = $Item.Split("%")[1]
            # 从用户变量和系统变量同时查找
            $BaseReal = [environment]::GetEnvironmentVariable($Base)
            $RealValue = $Item.Split("%")[0]+$BaseReal+$Item.Split("%")[2]
            if($OldValue.Contains($RealValue)){
                $OldValue= $OldValue.Replace($RealValue,$Item)
                Write-Host "PATH contains" $Item
                continue;
            }
        }

        if($OldValue.Contains($Item)){
            Write-Host "PATH contains" $Item
        } else {
            $flag = 1
            if($OldValue.Trim().EndsWith(";")){
                $OldValue=$OldValue+$Item
            } else {
                $OldValue=$OldValue+";"+$Item
            }
        
        }
    }

    if($flag -eq 1){
        [Environment]::SetEnvironmentVariable("Path", $OldValue, [System.EnvironmentVariableTarget]::Machine )
    }
}



Create-EnvVar -Name "GRADLE_USER_HOME" -Value "D:\Program Files (Dev)\Maven\gradleRepository"
Create-EnvVar -Name "M2_HOME" -Value "D:\Program Files (Dev)\Maven\repository"
Create-EnvVar -Name "MAVEN_HOME" -Value "D:\Program Files (Dev)\Maven\apache-maven-3.6.0"
Create-EnvVar -Name "JAVA_HOME" -Value "D:\Program Files (Dev)\Java\jdk1.8.0_201"
Create-EnvVar -Name "ANDROID_HOME" -Value "D:\Android\sdk"

$paths = @(
"%JAVA_HOME%\bin",
"%MAVEN_HOME%\bin",
"D:\Program Files (Dev)\Git\bin",
"D:\Android\sdk\platform-tools",
"D:\Program Files (Dev)\Python37",
"D:\Program Files (Dev)\Python37\Scripts",
"D:\Program Files (Dev)\Maven\apache-maven-3.6.0\bin"
)

Append-PATH -Paths $paths

# read-host
pause