#!/bin/bash

echo ""
echo "..........................."
echo "Running test_2_cfginfo.sh"
echo "..........................."
echo ""

echo "Querying the configurations"
cli/cfginfo > grading/cli_tests/obtained_cfginfo.txt

if [ $? -eq 0 ]; then
    cmp -s grading/cli_tests/expected_cfginfo.txt grading/cli_tests/obtained_cfginfo.txt
	if [ $? -eq 0 ]; then
        echo "Obtained = Expected. Passed."
    else
        echo "Obtained != Expected. Failed."
        exit 1
    fi
else
	echo "cfginfo returned failure"
	exit 1
fi

