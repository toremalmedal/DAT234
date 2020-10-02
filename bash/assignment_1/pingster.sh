#!/bin/bash

function ping_ips(){
## Checks if input looks like a IP4-address
## Supports 4 period separated numbers with 1 to 3 digits.
## TODO: 111111.11.11.111111, or 99.99.99.99 etc returns true

if [[ $1 =~ [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} ]]; then

    # Stores the first three octets
    BASE_IP=$(echo $1 | grep -oP "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.")
    
    echo "$1 is valid. Will ping IP range ${BASE_IP}0/24"
    
    # Adds last octet to IP and pings the address:
    for i in {1..255}; do
        CURRENT_IP=$BASE_IP$i
        echo "Pinging $CURRENT_IP"
        ping -c 1 -W 2 $CURRENT_IP > ping_results
        # Prints contents of file in every loop to avoid the user having to wait
        # minutes before seeing a response.
        cat ping_results | grep "1 received"
    done

    rm ping_results

else
    echo "$1 is not valid"
fi
}

if [ -z "$1" ];then
    while :; do
        echo -n "Please enter an IPv4-address ('q' for quit)"; read IP;

        if [ "$IP" == "q" ]; then
            break
        else
            ping_ips "$IP"
        fi
    done
# If script is run with an argument, it is used instead of waiting for input
else
    ping_ips "$1"
fi