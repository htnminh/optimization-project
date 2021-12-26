#!/bin/bash
# please run this from root of source code:
#
# ~/optimization-project$ scripts/run-all_MIP.sh

# change dir to root of project
cd $PWD

outdir=scripts/output/out_MIP
analyzedir=scripts/output/analyze_MIP

# create output folder
mkdir -p $outdir
mkdir -p $analyzedir

# find all states and store in an array
x=$(cd files/generated_data; find . -name "*.txt" | awk '{print substr($0, 3)}' | sort )

for i in $x; do
	# sanity check
	echo "ping: $i";
	
	# in order: file for algo output, output parser, input for algo
	file="$outdir/out_MIP_$i";
	analyze="$analyzedir/analyze_MIP_$i";
	filepath="files/generated_data/$i"
	
	# create file for algo output and output parser
	touch $file;
	touch $analyze;
	
	# execute CPM & time it
	/usr/bin/time -f "time: %e" -ao $file python3 files/mip_model.py $filepath > $file;
	
done

# run parser & converter
bash scripts/parse-output.sh MIP
