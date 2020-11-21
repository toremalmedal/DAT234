Param(
    [Parameter(Mandatory=$true)]
    [string]$ip,
    [string]$subnet
)

function PingRange($ip_binary, $netmask){
    # Separates out the network part that will remain the same, and the 
    # part that will define each host
    $network = $ip_binary.Substring(0, $netmask)
    
    #We want to know how many IPs we have in our range:
    $range = [convert]::ToInt32("1" * (32-$netmask),2)

    for ($i=1; $i -le $range; $i++){

        # Convert the range into binary string, pads with zeroes to correct size
        $host_ip = ([convert]::toString($i, 2)).padleft(32-$netmask, "0")
        # Concatenate basestring and host-specific string
        $this_ip = $network + $host_ip
        $this_ip = ConvertToDecimal $this_ip

        Write-Host "Pinging $this_ip"
        Test-Connection -Count 1 -IPv4 -TimeoutSeconds 1 $this_ip
    }
}

# We want to convert our IP-adress to binary, so that we can more
# easily work with the subnet bits

function ConvertToBinary($ip_dotted){
    $octets = $ip_dotted -Split "\."
    # Convert each octet to binary with leading 0, concatenate to ip_binary
    foreach($octet in $octets){
        $octet = [convert]::toString($octet, 2)
        $octet = $octet.padleft(8,"0")
        $ip_binary += $octet
    }
    return $ip_binary
}

function ConvertToDecimal($ip_binary){
    # Converts each binary octet to decimal, separates with dots for three first octets 
    # https://devblogs.microsoft.com/scripting/use-powershell-to-easily-convert-decimal-to-binary-and-back/
    $octets = [regex]::matches($ip_binary,'\d{8}').value
    $i = 0
    foreach($octet in $octets){
        $octet = [convert]::ToInt32($octet,2)
        [string]$ip_dotted += $octet
        if($i -le 2){
            $ip_dotted += "."
        }
        $i++
    }
    return $ip_dotted
}

# If subnet is in cidr notation we assume no subnet param is passed
if (([string]::IsNullOrEmpty($subnet)))
{
    $subnet = ($ip -Split "\/")[1]
    $ip = ($ip -Split "\/")[0]
}
# If subnet is in decimal we convert to cidr
else 
{
    $subnet = ConvertToBinary $subnet   
    $subnet = ([regex]::Matches($subnet, "1" )).count
}

# Convert dotted ip to binary:
$ip_binary = ConvertToBinary $ip
PingRange $ip_binary $subnet
