Set-Alias gh Get-Help;
Set-Alias cd Push-Location -Option AllScope;
Set-Alias cdb Pop-Location -Option AllScope;

Set-PSReadLineOption -HistoryNoDuplicates;

$ProjectDirectory = 'C:\Projects';

function cdp {
	[CmdletBinding()]
    Param()

    DynamicParam {
        # Set the dynamic parameters' name
        $ParameterName = 'Path';

        # Create the dictionary
        $RuntimeParameterDictionary = New-Object System.Management.Automation.RuntimeDefinedParameterDictionary;

        # Generate and set the ValidateSet
        $DirectorySet = Get-ChildItem -Path $ProjectDirectory -Directory | Select-Object -ExpandProperty Name;
        $ValidateSetAttribute = New-Object System.Management.Automation.ValidateSetAttribute($DirectorySet);

        # Create and set the parameters' attributes
        $ParameterAttribute = New-Object System.Management.Automation.ParameterAttribute;
        $ParameterAttribute.Position = 0;

        # Create the collection of attributes
        $AttributeCollection = New-Object System.Collections.ObjectModel.Collection[System.Attribute];
		$AttributeCollection.Add($ValidateSetAttribute);
		$AttributeCollection.Add($ParameterAttribute);

        # Create and return the dynamic parameter
        $RuntimeParameter = New-Object System.Management.Automation.RuntimeDefinedParameter($ParameterName, [string], $AttributeCollection);
        $RuntimeParameterDictionary.Add($ParameterName, $RuntimeParameter);

        return $RuntimeParameterDictionary;
    }

    Begin {
        # Bind the parameter to a friendly variable
        $ProjectName = $PsBoundParameters[$ParameterName];
    }

    Process {
		cd $ProjectDirectory\$ProjectName;
    }
}

function cdh {
    cd ~;
}

Push-Location (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent);

Import-Module posh-git;

$Global:GitPromptSettings.BeforeText = ' ';
$Global:GitPromptSettings.BeforeForegroundColor = [ConsoleColor]::DarkGray;
$Global:GitPromptSettings.BeforeBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.DelimText = " $([char]0xb7)";
$Global:GitPromptSettings.DelimForegroundColor = [ConsoleColor]::DarkGray;
$Global:GitPromptSettings.DelimBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.AfterText = ' ';
$Global:GitPromptSettings.AfterForegroundColor = [ConsoleColor]::DarkGray;
$Global:GitPromptSettings.AfterBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.LocalStagedStatusForegroundColor = [ConsoleColor]::DarkGray;
$Global:GitPromptSettings.LocalStagedStatusBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.BranchForegroundColor = [ConsoleColor]::DarkGray;
$Global:GitPromptSettings.BranchBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.BranchIdenticalStatusToForegroundColor = [ConsoleColor]::DarkGray;
$Global:GitPromptSettings.BranchIdenticalStatusToBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.BranchBehindAndAheadStatusForegroundColor = [ConsoleColor]::DarkYellow;
$Global:GitPromptSettings.BranchBehindAndAheadStatusBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.BranchBehindStatusForegroundColor = [ConsoleColor]::DarkRed;
$Global:GitPromptSettings.BranchBehindStatusBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.BranchAheadStatusForegroundColor = [ConsoleColor]::DarkGreen;
$Global:GitPromptSettings.BranchAheadStatusBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.LocalWorkingStatusBackgroundColor = [ConsoleColor]::White;
$Global:GitPromptSettings.BeforeIndexBackgroundColor = [ConsoleColor]::White;
$Global:GitPromptSettings.IndexBackgroundColor = [ConsoleColor]::White;
$Global:GitPromptSettings.WorkingBackgroundColor = [ConsoleColor]::White;

$Global:GitPromptSettings.EnableWindowTitle = $false;
$Global:GitPromptSettings.ShowStatusWhenZero = $false;

# Set up a simple prompt, adding the git prompt parts inside git repos
function global:prompt {
    $realLASTEXITCODE = $Global:LASTEXITCODE;
    $hostline = " $env:Username@$env:UserDomain ";

    Write-Host;

    if ($realLASTEXITCODE -eq 0) {
        $hostColor = [ConsoleColor]::DarkGreen;
    } else {
        $hostColor = [ConsoleColor]::DarkRed;
        $hostline += "(0x$('{0:X0}' -f $realLASTEXITCODE)) ";
    }

    Write-Host $hostline -ForegroundColor White -BackgroundColor $hostColor -NoNewLine;
    Write-Host "$([char]0xe0b0)" -ForegroundColor $hostColor -BackgroundColor DarkGray -NoNewline;

    $realFolderName = (Get-Item $pwd.ProviderPath).Name;

    if ($pwd.ProviderPath -eq $env:UserProfile) {
        $folderName = '~';
    } else {
        $folderName = $realFolderName;
    }

    Write-Host " $folderName " -ForegroundColor White -BackgroundColor DarkGray -NoNewline;

    $gitStatus = Get-GitStatus;

    if ($gitStatus -ne $null) {
        Write-Host "$([char]0xe0b0)" -ForegroundColor DarkGray -BackgroundColor White -NoNewline;
        Write-GitStatus $gitStatus;
        Write-Host "$([char]0xe0b0)" -ForegroundColor White;
    } else {
        Write-Host "$([char]0xe0b0)" -ForegroundColor DarkGray;
    }

    $Global:LASTEXITCODE = 0;

    Write-Host " PS " -ForegroundColor DarkGray -BackgroundColor White -NoNewline;
    Write-Host "$([char]0xe0b0)" -ForegroundColor White -NoNewline;

    Write " ";

    try {
        & "$env:ConEmuBaseDir\ConEmuC.exe" "/GUIMACRO", 'Rename(0,@"'$realFolderName'")' > $null;
    } catch { }
}

Pop-Location;

Start-SshAgent -Quiet;
