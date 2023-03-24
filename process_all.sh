#!/bin/bash

num=0
for result in ./results/*.results; do
	echo -n "Processing data for $result..."
	python3 ./process_result.py --silent $result
	success=$?
	if ((success == 0)); then
		num+=1
		echo "done"
	else
		echo "ID already processed"
	fi
done

echo "Processed $num new files"