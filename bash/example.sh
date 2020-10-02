#!/bin/bash

echo "Count to ten"
for count in {1..10}
do
	echo Writing $count to file
	echo $count >> count.txt
done

echo "Replace 10 with 9001"
echo "9001" | cut -10 -d ' '

#Example using functions
dirExists (){
if [[ -d $1 ]]; then
	echo "Found em $1"
else
	echo "Could not find directory, creating one"
	mkdir -p $1
fi
}

