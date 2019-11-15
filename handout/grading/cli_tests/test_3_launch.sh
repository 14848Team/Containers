#!/bin/bash

echo ""
echo "..........................."
echo "Running test_3_launch.sh"
echo "..........................."
echo ""

echo "Launching one instance using config tiny-1-1.cfg"
cli/launch tiny 1 1

if [ $? -eq 0 ]; then
    wget http://localhost:8000
	if [ $? -eq 0 ]; then
        echo "Webserver running. Passed."
    else
        echo "Webserver not running. Failed"
        exit 1
	fi
else
	echo "launch returned failure"
	exit 1
fi

echo "Launching another instance using config tiny-2-2.cfg"
cli/launch tiny 2 2

if [ $? -eq 0 ]; then
    wget http://localhost:7070
    if [ $? -eq 0 ]; then
        echo "Webserver running. Passed."
    else
        echo "Webserver not running. Failed"
        exit 1
    fi
else
    echo "launch script returned failure"
    exit 1
fi

