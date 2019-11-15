#!/bin/bash

echo ""
echo "..........................."
echo "Running test_1_upload.sh"
echo "..........................."
echo ""

echo "Uploading tiny-1-1.cfg"
cli/upload grading/cli_tests/configs/tiny-1-1.cfg

if [ $? -eq 0 ]; then
	echo "upload returned success"
else
	echo "upload returned failure"
	exit 1
fi

echo "Uploading tiny-2-2.cfg"
cli/upload grading/cli_tests/configs/tiny-2-2.cfg

if [ $? -eq 0 ]; then
    echo "upload returned success"
else
    echo "upload returned failure"
	exit 1
fi

echo "Uploading tiny-3-3.cfg"
cli/upload grading/cli_tests/configs/tiny-3-3.cfg

if [ $? -eq 0 ]; then
    echo "upload returned success"
else
    echo "upload returned failure"
	exit 1
fi

