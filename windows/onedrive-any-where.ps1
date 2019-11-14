# 
function Select-FolderDialog{
    param([string] $Directory,[string] $Description)

    [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null
    $objForm = New-Object System.Windows.Forms.FolderBrowserDialog
    $objForm.RootFolder = $Directory
    $objForm.Description = $Description
    $objForm.ShowNewFolderButton = $false
    $Show = $objForm.ShowDialog()

    If ($Show -eq "OK") {
        Return $objForm.SelectedPath
    } Else{
        #需要输出错误信息的话可以取消下一行的注释
        #Write-Error "error information here"
    }
}

$folder_path = Select-FolderDialog -Directory "Desktop" -Description "请选择要同步到OneDrive的文件夹"
Write-Host "将要把" $folder_path "文件夹同步到 Onedrive"

pause