#!/bin/bash

echo ""
echo "..........................."
echo "Running test_4_list.sh"
echo "..........................."
echo ""

echo "Listing the instances"
cli/list > grading/cli_tests/obtained_list.txt

if [ $? -eq 0 ]; then
    if [[ $(wc -l < grading/cli_tests/obtained_list.txt) -ge 2 ]]; then
	   echo "Passed"
    else
        echo "Failed"
	fi
else
	echo "list returned failure"
	exit 1
fi

