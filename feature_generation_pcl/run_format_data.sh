#! /bin/bash

set -e    # Stop on errors
set -x    # Show commands as they are executed

DIR=$1
M=$2
rm -f scripts/data_*
cp data_* scripts/
cp Segmentation_labeling.txt scripts/

CWD=$(pwd)

cd scripts
rm -f nohup.out
nohup matlab -nodesktop -nosplash -r binfeats


perl format_svm_seg.pl Segmentation_labeling.txt . 1
mkdir segments
perl createSegmentsFiles.pl $DIR $M
mkdir -p $DIR/segments/$M
mv -f segments/* $DIR/segments/$M
mkdir -p $DIR/data/$M
mv -f  0*txt $DIR/data/$M
mv -f  1*txt $DIR/data/$M

rm Segmentation_labeling.txt
rm data_*
rm -r segments
cd ..

