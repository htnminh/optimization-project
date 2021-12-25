#!/bin/bash
# usage:
# :~ $ $(PWD)/script_parse-output.sh <MODE> <FILE_TO_PARSE> <OUTPUT> <MANUAL_OR_AUTO>
#
# where:
#	<MODE> = MIP | CPM
#	<FILE_TO_PARSE> = $(PWD)/output/out_$MODE/file.txt
#	<OUTPUT> = $(PWD)/output/analyze_$MODE/file.txt
#	<MANUAL_OR_AUTO> = 0 | 1
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
manual=$4 #

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
	f=$(cd files/generated_data/; find . -name "*.txt" | awk '{print substr($0, 3)}' | sort )
	csvdir=scripts/output/$mode
	csvfile=$csvdir/analyze_$mode.csv

	mkdir -p $csvdir	
	echo "n_rect,n_car,cost,n_car_used,time_limit,time_running" > $csvfile

	for i in $f; do
		file="scripts/output/out_MIP/out_MIP_$i";
		analyze="scripts/output/analyze_MIP/analyze_MIP_$i";
		filepath="files/generated_data/$i";
		PKG=$(cat $filepath | head -n1 | awk '{print $1}');
		CAR=$(cat $filepath | head -n1 | awk '{print $2}');
		CST=$(cat $file | head -n1 | awk '{print $3}');
		TME=$(cat $file | tail -n1 | awk '{print $2}');
		if [ ! -z "$CST" ]; then
			CUS=$(cat $file | tail -n2 | head -n1 | awk '{print $2}');
		fi
		echo $PKG >  $analyze; # n pkgs
		echo $CAR >> $analyze; # n cars
		echo $CST >> $analyze; # min cost
		echo 300  >> $analyze; # time limit
		echo $TME >> $analyze; # time elapsed
		echo $CUS >> $analyze; # n car used
		echo "$PKG,$CAR,$CST,$CUS,300.0,$TME" >> $csvfile
		
		
	done
	## DATA
	#cat $input | grep "put" | awk '{print $3, $6, $9, $12, $15}' >> $output
fi

# ping
echo "written $output"
