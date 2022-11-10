#!/bin/sh
for script in *.py
do
	python3 $script &
	echo $! >> ./pid.txt
done