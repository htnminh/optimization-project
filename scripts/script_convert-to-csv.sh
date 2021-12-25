#!/bin/bash
# change dir to root of project
cd $PWD

# READ
mode=$1   # CPM, MIP
input=$(find scripts/output/analyze_$mode/ -name "*.txt" | sort )

# OUTPUT
if ! [ -d "scripts/output/$mode" ]
then
	mkdir -p scripts/output/$mode/;
fi

# csv file
csvfile=scripts/output/$mode/analyze_$mode.csv
if ! [ -f "$csvfile" ];
then
	touch $csvfile;
fi

echo "n_rect,n_car,cost,n_car_used,time_limit,time_running" > $csvfile

# MODE: CPM
if [ $mode == CPM ];
then
	for i in $input; do
		## N_RECT	
		cat $i | awk '{if(NR==4){printf "%s", $0}}' >> $csvfile;
		echo -n "," >> $csvfile;
		
		## N_CAR
		cat $i | awk '{if(NR==3){printf "%s", $0}}' >> $csvfile;
		echo -n "," >> $csvfile;
		
		## COST
		cat $i | awk '{if(NR==1){printf "%s", $0}}' >> $csvfile;
		echo -n "," >> $csvfile;
		
		## N_CAR_USED
		cat $i | awk '{if(NR==6){printf "%s", $0}}' >> $csvfile;
		echo -n "," >> $csvfile;
		
		## TIME_LIMIT
		cat $i | awk '{if(NR==2){printf "%s", $0}}' >> $csvfile;
		echo -n "," >> $csvfile;
		
		## TIME_RUNNING
		cat $i | awk '{if(NR==5){printf "%s", $0}}' >> $csvfile;
		echo >> $csvfile;
	done
fi
