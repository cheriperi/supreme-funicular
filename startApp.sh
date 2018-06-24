#!/bin/bash

executingDHT="false"

function tmp (){
	
	if [ "$1" = "false" ]
	then
		echo "executing dht"
		xterm -e 'python3 dhtPub.py' &
	fi
	xterm -e 'python3 tmpSub.py' &
}

function hum () {
	if [ "$1" = "false" ]
	then
		xterm -e 'python3 dhtPub.py' &
	fi
	xterm -e 'python3 humSub.py' &
}

function ldr () {

	xterm -e 'python3 ldrPub.py' &
	xterm -e 'python3 ldrSub.py' &
}

if [ "$#" -gt 1 ] 
then
	echo "invalid number of arguments"
	
else
	if [ "$#" -eq 0 ] || [ "$1" = "all" ]
	then 
		echo "Executing all the modules"
		tmp $executingDHT
		executingDHT="true"
		hum $executingDHT
		ldr
	elif [ "$1" = "tmp" ]
	then
		echo "Executing tmp"
		tmp $executingDHT
		executingDHT="true"
		
	elif [ "$1" = "hum" ]
	then	
		echo "Executing hum"
		hum $executingDHT
		executingDHT="true"
		
	elif [ "$1" = "ldr" ]
	then	
		echo "Executing ldr"
		ldr
	else
		echo "modulo incorrecto. Puede usar all, tmp, hum o ldr"
	fi
fi

