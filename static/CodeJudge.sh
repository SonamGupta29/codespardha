#!/bin/bash
# exit =1 means CTE
# exit =2 means RTE
# exit =3 means TIme limit exceeded
# exit =4 means Wrong Answer
# exit =5 means Accepted
# input $1 = c file path $2 = test case file path $3 = output match file path

if [[ ! -f $1 ]]; then
	echo "Not a File"
	exit 1
fi
g++ $1 1>/dev/null 2>&1

if [[ $? -ne 0 ]]; then
	echo "CTE"
	exit 1
fi

{ timelimit -t3 ./a.out < $2; } 1>/dev/null 2>&1

if [[ $? -ne 0 ]]; then
	if [[ $? -eq 139 ]]; then
		echo "Segmentation Fault"
		exit 2
	fi
	echo "RTE"
	exit 3

fi

if [[ ! -f $2 ]]; then
	echo "Test FIle Not Found"
	exit 1
fi
if [[ ! -f $3 ]]; then
	echo "Output FIle Not Found"
	exit 1
fi

./a.out < $2 > tempoutput 2>/dev/null

diff -u tempoutput "$3"

if [[ $? -eq 0 ]]; then
	echo "Accepted"
	exit 5

else echo "Wrong Answer"
	echo $?
	exit 4
fi