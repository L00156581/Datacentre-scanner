#Requires -runasadministrator
# Create-DatacentreLab.ps1
# Automates the creation of an isolated Hyper-V lab to simulate a data centre environemnt.
# The lab will be used to safely test security assessment scripts.

# Stop script immediately if any command fails.
$ErrorActionPreference = "Stop"


# 1. GLOBAL PATHS AND SETTINGS
$SwitchName = "DC-Lab-Switch" # Identify private virtual network switch.
$LabPath = Join-Path $PSScriptRoot "Datacentre-Lab" # Automatically find where script is saved and create main lab folder there.
$VMPath = "$LabPath\VMs" # Create a subfolder to store the virtual machine configuration files.
$VHDPath = "$LabPath\Virtual Hard Disks" # Create a subfolder to store the virtual hard drives (.vhdx files).
$ISOPath = Join-Path $LabPath "ISO" # Create an ISO sub folder for users to drop their OS installer files.

# 2. VM CONFIGURATION
# An array containing hash-tables to programmatically structure our target infrastructure.
$VMs = @(
    @{
        Name       = "Assessment-VM"    # Attacker machine (Kali Linux)
        Memory     = 4GB                # Volatile memory allocation
        CPUs       = 2                  # Processing core allocation
        DiskSize   = 40GB               # Static storage allocation 
    },
    @{
        Name       = "WebServer"        # Target A: Web server
        Memory     = 2GB
        CPUs       = 2
        DiskSize   = 20GB
    },
    @{
        Name       = "WindowsServer"    # Target B: Active Directory services
        Memory     = 4GB
        CPUs       = 2
        DiskSize   = 60GB
    },
    @{
        Name       = "DatabaseServer"   # Target C: Misconfigured MySQL database
        Memory     = 4GB
        CPUs       = 2
        DiskSize   = 30GB
    }
)

# 3. CREATE STORAGE DIRECTORIES
Write-Host ""
Write-Host "Creating laboratory directories..." -ForegroundColor green
# Create folders
New-Item -ItemType Directory -Path $LabPath -Force
New-Item -ItemType Directory -Path $VMPath -Force 
New-Item -ItemType Directory -Path $VHDPath -Force 
New-Item -ItemType Directory -Path $ISOPath -Force


# 4. CREATE ISOLATED SWITCH
Write-Host ""
Write-Host "Creating isolated Hyper-V switch..." -ForegroundColor green
$ExistingSwitch = Get-VMSwitch -Name $SwitchName -ErrorAction SilentlyContin # Check if switch lready exists 

# If the switch does not exist cerate a new one.
if (-not $ExistingSwitch) {

    # Create a 'Private' switch type. 
    # VMs on this switch can communicate with each other but have no internet access.
    New-VMSwitch `
        -Name $SwitchName `
        -SwitchType Private

    Write-Host "Created private switch: $SwitchName" -ForegroundColor Green

}else {
    # If the switch exists, notify the user and bypass.
    Write-Host "Switch already exists: $SwitchName" -ForegroundColor Yellow
}

# 5. CREATE VIRTUAL MACHINES

# Loop to extract server definition from data dictionary array and apply parameters.
foreach ($VM in $VMs) {

    $Name     = $VM.Name
    $Memory   = $VM.Memory
    $CPUs     = $VM.CPUs
    $DiskSize = $VM.DiskSize

    # Use Join-Path to construct safe, non-broken OS directory paths automatically.
    $VMDirectory = Join-Path $VMPath $Name
    $VHD         = Join-Path $VHDPath "$Name.vhdx"

    Write-Host ""
    Write-Host "Creating $Name..." -ForegroundColor green

    # Skip this VM if it already exists from previous run.
    if (Get-VM -Name $Name -ErrorAction SilentlyContinue) {
        Write-Host "$Name already exists - skipping." -ForegroundColor Yellow
        continue #
    }

    # Create a dedicated subfolder for virtual machine metadata.
    New-Item `
        -ItemType Directory `
        -Path $VMDirectory `
        -Force 

    # Build new Generation 2 Virtual Machine connected to isolated switch.    
    New-VM `
        -Name $Name `
        -Generation 2 `
        -MemoryStartupBytes $Memory `
        -NewVHDPath $VHD `
        -NewVHDSizeBytes $DiskSize `
        -Path $VMDirectory `
        -SwitchName $SwitchName | Out-Null

    # Allocate CPU core count.
    Set-VMProcessor `
        -VMName $Name `
        -Count $CPUs

    # Turn off dynamic RAM so experimental speed tests stay accurate
    Set-VMMemory `
        -VMName $Name `
        -DynamicMemoryEnabled $false
    # Set VM to turn off gracefully if the host computer restarts
    Set-VM `
        -Name $Name `
        -AutomaticStopAction ShutDown

    Write-Host "$Name created successfully." -ForegroundColor Green
}

# 6. DISPLAY FINAL LAB SUMMARY
Write-Host ""
Write-Host "==========================================" -ForegroundColor green
Write-Host " Hyper-V Data Centre Lab Created"
Write-Host "==========================================" -ForegroundColor green

# Print status table of the new VM's.
Get-VM |
    Where-Object {
        $_.Name -in $VMs.Name
    } |
    Select-Object Name, State, CPUUsage, MemoryAssigned, Generation |
    Format-Table -AutoSize # Auto-adjust column sizes for readability.

Write-Host ""
Write-Host "Virtual switch:" -ForegroundColor green

# Print status table of isolated switch.
Get-VMSwitch -Name $SwitchName |
    Select-Object Name, SwitchType, NetAdapterName |
    Format-Table -AutoSize

# Print final confirmation details
Write-Host ""
Write-Host "Lab location: $LabPath" -ForegroundColor Green
Write-Host "Switch: $SwitchName" -ForegroundColor Green
Write-Host "Subnet: 192.168.10.0/24" -ForegroundColor Green
Write-Host ""
Write-Host "VM creation complete." -ForegroundColor Green
