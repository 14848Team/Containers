#!/bin/bash

echo ""
echo "............................"
echo "Running test_5_destroyall.sh"
echo "............................"
echo ""

echo "Calling destroy all"
cli/destroyall

if [ $? -eq 0 ]; then
	wget http://localhost:8000
	if [ $? -eq 0 ]; then
        echo "Webserver still running. Failed."
        exit 1
    else
    	wget http://localhost:7070
    	if [ $? -eq 0 ]; then
        	echo "Webserver still running. Failed"
        	exit 1
        else
        	echo "Both webservers terminated. Passed"
        fi
	fi
else
	echo "destroyall returned failure"
	exit 1
fi

