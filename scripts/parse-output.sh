#!/bin/bash
# usage:
# :~ $ $(PWD)/script_parse-output.sh <MODE>
#
# where:
#	<MODE> = MIP | CPM
#
# input:
#	out_<MODE>/*
#
# output:
# < to analyze/analyze_<MODE>_<input>.txt
# 	<MIN_COST>
#	<TIME_LIM>
#	<N_TRUCKS>
#	<N_RECTS>
#	<TIME_RUN>
#	<N_TRUCKS_USED>
#
# < to analyze_<MODE>.csv
#	n_rect,n_car,cost,n_car_used,time_limit,time_running
#
# change dir to root of project
cd $PWD

# READ
mode=$1   # CPM, MIP

# MODE: CPM
if [ $mode == "CPM" ];
then
	# list all pre-gen states
	f=$(cd files/generated_data/; find . -name "*.txt" | awk '{print substr($0, 3)}' | sort )

	# CSV stuff
	csvdir=scripts/output/csv_$mode
	csvfile=$csvdir/analyze_$mode.csv
	mkdir -p $csvdir	
	echo "n_rect,n_car,cost,n_car_used,time_limit,time_running" > $csvfile

	for i in $f; do
		# file shortcut
		file="scripts/output/out_$mode/out_$mode_$i";           # data to read from
		analyze="scripts/output/analyze_$mode/analyze_MIP_$i";  # write to
		filepath="files/generated_data/$i";                     # read some info directly from input
		ret=$(cat $file | tail -n7)                             # return info from CPM program

		# order: n_rects, n_cars, sanity test
		PKG=$(cat $filepath | head -n1 | awk '{print $1}');
		CAR=$(cat $filepath | head -n1 | awk '{print $2}');
		CUS=$(cat $filepath | head -n1 | awk '{print $1}');
		
		# if $CUS is read, is not "command" in command terminated by/with ...,
		# a solution was found, read other stats
		if [ ! -z "$CUS" ] || [ $CUS != "command" ] ; then
			CUS=$(cat $ret | head -n1 | awk '{print $5}');           # n_used
			CST=$(cat $ret | awk '{if (NR==2) {printf "%s", $2}}');  # cost
			STT=$(cat $ret | awk '{if (NR==4) {printf "%s", $3}}');  # status (OPT/FEA)
			BRC=$(cat $ret | awk '{if (NR==5) {printf "%s", $4}}');  # branching factor
			IFT=$(cat $ret | awk '{if (NR==6) {printf "%s", $3}}');  # In-file running time | might not be reflective
			TME=$(cat $ret | awk '{if (NR==7) {printf "%s", $2}}');  # Bash-measured time | using /usr/bin/time, real
			#
			# running data set 0120: 
			# $ time python3 files/cp_model.py p/t/0120.txt
			#
			# Running time: 600.267035276 seconds    <-- python3's measurement
			# real	10m4,562s                        <-- Bash-monitored running time
			# user	39m33,397s                       <-- CPU-time. user/4 ~= average time all 4-core of CPU are used
			#                                            (OR-Tools has multi-threading)
		fi		
		
		# analyze
		echo $PKG >  $analyze; # n pkgs
		echo $CAR >> $analyze; # n cars
		echo $CST >> $analyze; # min cost
		echo 300  >> $analyze; # time limit, defaulted 300
		echo $TME >> $analyze; # time elapsed
		echo $CUS >> $analyze; # n car used
	done
fi

# MODE: MIP
if [ $mode == MIP ];
then
	# list all pre-gen states
	f=$(cd files/generated_data/; find . -name "*.txt" | awk '{print substr($0, 3)}' | sort )
	
	# CSV stuff
	csvdir=scripts/output/$mode
	csvfile=$csvdir/csv_$mode.csv
	mkdir -p $csvdir	
	echo "n_rect,n_car,cost,n_car_used,time_limit,time_running" > $csvfile


	for i in $f; do
		# file shortcut
		file="scripts/output/out_MIP/out_MIP_$i";             # data to read from
		analyze="scripts/output/analyze_MIP/analyze_MIP_$i";  # write to
		filepath="files/generated_data/$i";                   # read some info directly from input
		
		# order: n_rects, n_cars, min_cost, r_time
		PKG=$(cat $filepath | head -n1 | awk '{print $1}');
		CAR=$(cat $filepath | head -n1 | awk '{print $2}');
		CUS=$(cat $file | head -n1 | awk '{print $3}');
		TME=$(cat $file | tail -n1 | awk '{print $2}');
		
		# if $CUS is read, is not "by" or "with" in command terminated by/with ...,
		# a solution was found, read its CAR_USED
		if [ ! -z "$CUS" ] || [ $CUS != "by" ] || [ $CUS != "with" ] ; then
			CUS=$(cat $file | tail -n2 | head -n1 | awk '{print $2}');
		fi
		
		# analyze
		echo $PKG >  $analyze; # n pkgs
		echo $CAR >> $analyze; # n cars
		echo $CST >> $analyze; # min cost
		echo 300  >> $analyze; # time limit, defaulted 300
		echo $TME >> $analyze; # time elapsed
		echo $CUS >> $analyze; # n car used
		
		# output to CSV
		echo "$PKG,$CAR,$CST,$CUS,300.0,$TME" >> $csvfile;
	done
fi

# ping
# output to CSV
echo "$PKG,$CAR,$CUS,$CUS,300.0,$TME" >> $csvfile;
echo "written"
