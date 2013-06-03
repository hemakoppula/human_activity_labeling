DIR=$1
M=$2
rm scripts/data_*
cp data_* scripts/
cp Segmentation_labeling.txt scripts/

cd scripts
rm -f nohup.out
nohup matlab -nodesktop -nosplash -r binfeats


perl format_svm_seg.pl Segmentation_labeling.txt . 1
mkdir segments
perl createSegmentsFiles.pl '/opt/ros/electric/stacks' $M
mkdir -p $DIR/segments/$M
mv -f segments/* $DIR/segments/$M
mkdir -p $DIR/data/$M
mv -f  0*txt $DIR/data/$M
mv -f  1*txt $DIR/data/$M

rm Segmentation_labeling.txt
rm data_*
rm -r segments
cd ..

