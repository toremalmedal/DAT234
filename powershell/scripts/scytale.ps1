$splash="
 ____             ____        _ _
/ ___|  ___ _   _| __ )  __ _(_) |
\___ \ / __| | | |  _ \ / _` | | |
 ___) | (__| |_| | |_) | (_| | | |
|____/ \___|\__, |____/ \__,_|_|_|
            |___/Free that message!
"

function Show-Menu{
    Clear-Host
    Write-Host "$splash"
    Write-Host "Press '1' for encryption"
    Write-Host "Press '2' for decryption"
    Write-Host "Press 'q' to quit"
}

function Handle() {
    Param(
        [string]$mode,
        [int32]$key,
        [string]$message
    )

    Write-Host "Ciphering $message with key $key."
    # Copy paste fra 
    # https://github.com/nesadrian/Scytale-Cipher/blob/master/Scytale.ps1
    # Beskriv hvordan den fungerer.
    $new_message = ""
    foreach($j in 0..$key) {
        foreach($i in 0..$message.length){
            if($i % $key -eq $j){
                $new_message += $message[$i]
            }
        }
    }
    Write-Host $new_message
    pause
}

function Decipher(){
    # Copy paste fra 
    # https://github.com/nesadrian/Scytale-Cipher/blob/master/Scytale.ps1
    # Beskriv hvordan den fungerer.
    $new_message = ""

    $rows = $message.length/$key

    for($j = 0; $j -lt $rows; $j++) {
        for($i = 0; $i -lt $key; $i++) {
            if(($j * $key) + $i -lt ($message.length)) {
                $new_message += $message[$i * $rows + $j]
            }
        }
    }
    Write-Host $new_message
    pause
}

do
{
    Show-Menu
    $selection = Read-Host " Pick something! ('q' to quit) "
    switch ($selection)
    {
        '1' {
            [int32]$key = Read-Host ('Please enter key')
            $message = Read-Host ('Please enter string to encrypt')
            $mode = 'Ciphering'
            Handle $key $message
        } 
        '2' {
            [int32]$key = Read-Host ('Please enter key')
            $message = Read-Host ('Please enter string to decrypt')
            $mode = 'Deciphering'
            Decipher $key $message
        }
    }
} 
until ($selection -eq 'q')