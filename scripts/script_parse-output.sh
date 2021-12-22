#!/bin/bash

# change dir to root of project
SCRIPT_PATH=$(dirname $0)
cd $SCRIPT_PATH/..

# read
input=$1
output=$2

## COST
head -n1 < $input | awk '{print $3}' > $output

## TIME
tail -n1 < $input | awk '{print $2}' > $output

## data
cat $input | grep "put" | awk '{print $2, $4, $7, $10, $13}' > $output

# ping
echo "written to: $output"
