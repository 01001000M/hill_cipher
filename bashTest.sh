#!/bin/bash


if [[ "$1" == "-e" ]];then
	python3 ./enc.py $2 $3 $4 $5
fi

if [[ "$1" == '-d' ]];
then
	python3 ./dec.py $2 $3 $4 $5
fi

