#!/bin/sh

while read -r line
do
	echo "killing $line"
	kill -9 $line
done < "pid.txt"