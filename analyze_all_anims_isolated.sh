#!/bin/bash

num=0
for result in ./results/*/; do

	directory=${result%/}
	echo -n "Creating animations for $result..."
	python3 ./analyze_result_isolated.py --silent --noplots --noheats $directory
	success=$?
	if ((success == 0)); then
		((num++))
		echo "done"
	else
		echo "failed"
	fi
done

echo "Analyzed $num results successfully"