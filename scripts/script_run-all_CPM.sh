#!/bin/bash

# change dir to root of project
SCRIPT_PATH=$(dirname $0)
cd $SCRIPT_PATH/..

outdir=scripts/output/out_CPM
analyzedir=scripts/output/analyze_CPM

# create output folder
mkdir -p $outdir
mkdir -p $analyzedir

# find all states and store in an array
x=$(cd files/generated_data; find . -name "*.txt" | awk '{print substr($0, 3)}' | sort )

for i in $x; do
	# sanity check
	echo "ping: $i";
	
	# in order: file for algo output, output parser, input for algo
	file="$outdir/out_CPM_$i";
	analyze="$analyzedir/analyze_CPM_$i";
	filepath="files/generated_data/$i"
	
	# create file for algo output and output parser
	touch $file;
	touch $analyze;
	
	# execute CPM & time it
	/usr/bin/time -f "time: %Us" -ao $file python3 drafts/cp_model.py $filepath > $file;
	
	# run parser
	bash scripts/script_parse-output.sh $file $analyze;
done

# /usr/bin/time -f "time: %Us" -ao scripts/output/cp_model.txt python3 drafts/cp_model.py > scripts/output/cp_model.txt