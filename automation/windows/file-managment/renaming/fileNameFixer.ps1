#this script will remove the last three characters of the file name considering extention length

# Set the folder path
$folderPath = "F:\Shared Folder Daftar\Perseus Parts\compressed"


# Get all files in the folder
Get-ChildItem -Path $folderPath -File | ForEach-Object {
    # Get the file name without the extension
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    
    # Get the file extension
    $fileExtension = $_.Extension

    # Remove the last 3 characters from the file name
    if ($fileName.Length -gt 3) {
        $newFileName = $fileName.Substring(0, $fileName.Length - 4) + $fileExtension
        
        # Rename the file
        Rename-Item -Path $_.FullName -NewName $newFileName
    } else {
        Write-Host "File '$($_.Name)' is too short to modify."
    }
}
