function Show-Menu{
    Clear-Host
    Write-Host "Press '1' for encryption"
    Write-Host "Press '2' for decryption"
    Write-Host "Press 'q' to quit"
}

function Handle-Ciphering {
    Param(
        [int32]$key,
        [string]$message,
        [string]$mode
    )

    $printKey = [Math]::Abs($key)
    Write-Host "$mode $message with key $printKey." -ForegroundColor Green
    #TODO: Må deale med uppercase og skippe spesial-symbol
    #Quick-fixe: if-conditions checks if character is within range
    #A-Z [65-90]
    #a-z [97-122]

    $ascii_message = [int32[]][char[]]$message

    # Adds the modulu 26 of the integer of the message + key - char value of a (97):
    # This will make the letters "wrap around" if we reach the end of alphabet
    # Example XYZ, key = 3 will become 
    
    $handled_ascii = @()
    $handled_chars = @()

    foreach ($letter in $ascii_message) {
        # If the letter is 'space' (32), we leave it be
        if($letter -ge 65 -and $letter -le 90){
            $letter = $letter - 65 + $key
            # Modolus magic to handle negative numbers correctly
            $letter = (($letter % 26) + 26) % 26
            $letter = $letter + 65
        }
        elseif(($letter -ge 97) -and ($letter -le 122)){
            $letter = $letter - 97 + $key
            $letter = (($letter % 26) + 26) % 26
            $letter = $letter + 97
        }
        $handled_ascii += $letter
        $handled_chars += [char[]]($handled_ascii[-1])
    }
    Write-Host ($handled_chars -join '')
    pause
}

do
{
    Show-Menu
    $selection = Read-Host
    switch ($selection)
    {
        '1' {
            [int32]$key = Read-Host ('Please enter key')
            $message = Read-Host ('Please enter string to encrypt')
            $mode = "Ciphering"
            Handle-Ciphering $key $message $mode
        } 
        '2' {
            [int32]$key = Read-Host ('Please enter key')
            # Using negative key to reuse ciphering-code
            $key = -$key
            $message = Read-Host ('Please enter string to decrypt')
            $mode = "Deciphering"
            Handle-Ciphering $key $message $mode
        }
    }
} 
until ($selection -eq 'q')