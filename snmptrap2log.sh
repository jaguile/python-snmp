#!/bin/bash
# Escric els traps a un fitxer de logs
LOG_F=/var/log/trap.log

DATA=$(date +"%Y-%m-%d %T")

while read line; do
	echo "Capturat trap -- $DATA -- " >> $LOG_F
	echo "----------------------------------" >> $LOG_F
	echo "$line" >> $LOG_F
	echo "----------------------------------" >> $LOG_F
	echo >> $LOG_F
done