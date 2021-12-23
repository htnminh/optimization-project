#!/bin/bash
# usage:
# :~ $ $(PWD)/script_parse-output.sh <MODE> <FILE_TO_PARSE> <OUTPUT>
#
# where:
#	<MODE> = MIP | CPM
#	<FILE_TO_PARSE> = $(PWD)/output/out_$MODE/file.txt
#	<OUTPUT> = $(PWD)/output/analyze_$MODE/file.txt
#
# output:
# 	<MIN_COST>
#	<TIME_LIM>
#	<N_TRUCKS>
#	<N_RECTS>
#	<TIME_RUN>
#	<N_TRUCKS_USED>
#
# change dir to root of project
cd $PWD

# READ
mode=$1   # CPM, MIP
input=$2  # <FILE_TO_PARSE>
output=$3 # <OUTPUT>

# MODE: CPM
if [ $mode == "CPM" ];
then
	if [ $(cat $input | head -n1 | awk '{print $2}') == "terminated" ] || [  $(cat $input | head -n1 | awk '{print $1}') == "time" ] ; 
	then
		exit -1;
	fi

	ARR=()	
	
	## MIN_COST, TIME_LIM, N_TRUCKS, N_RECTS, TIME_RUN
	cat $input | tail -n5 | awk '{print $2}' > $output;

	## DATA: which trucks are used?
	#cat $input | grep "put" | awk '{print $3, $6, $9, $12, $15}';
	ARR+=$(cat $input | grep "put" | awk '{print $9}');
	UNIQ=($(for v in "${ARR[@]}"; do echo "$v"; done | sort | uniq | xargs));
	
	N_CAR_USED=${#UNIQ[@]}
	echo $N_CAR_USED >> $output
fi

# MODE: MIP
if [ $mode == MIP ];
then
	## COST
	cat $input | (head -n1 && tail -n1) > $output

	## DATA
	#cat $input | grep "put" | awk '{print $3, $6, $9, $12, $15}' >> $output
fi

# ping
echo "written $output"
