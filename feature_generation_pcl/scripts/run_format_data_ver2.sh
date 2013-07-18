#! /bin/bash

set -e    # Stop on errors
#set -x    # Show commands as they are executed



# Get args
if [ $# -lt 2 ]; then
  echo "Usage: `basename $0` <experiment directory> <method name>"
  echo
  echo "Parameters:"
  echo "  experiment directory: the directory containing data_*_feats.txt and Segmentation_labeling.txt. This is where the files data_*_feats.b.txt and directories formatted/{data,segments}/method_name will be created."
  echo "  method name: a descriptive string used to name the output directory"
  echo
  echo "Probably run this from the feature_generation_pcl directory like this:"
  echo "  $ scripts/run_format_data_ver2.sh ..."
  echo "or, if running Matlab with XVFB (for headless systems), run something like this (change :2 depending on your setup)"
  echo "  $ DISPLAY=:2 scripts/run_format_data_ver2.sh ..."
  exit 1
fi

experiment_dir="$1"
method="$2"



# Sanity checks for necessary files, set up links to executable and data directory
cd "$experiment_dir"         || ( echo "$experiment_dir does not exist. Create it first."; exit 1 )
filenames="Segmentation_labeling.txt data_obj_feats.txt data_obj_obj_feats.txt data_skel_feats.txt data_skel_obj_feats.txt data_temporal_obj_feats.txt data_temporal_skel_feats.txt"
for filename in $filenames; do
    ls $filename || ( echo "Could not find '$filename' file in $experiment_dir. Create it first."; exit 1 )
done
ln -fs "../scripts/binfeats.m"
ln -fs "../scripts/getBinStumps.m"
ln -fs "../scripts/classmap.txt"
ln -fs "../scripts/affmap.txt"
ls binfeats.m getBinStumps.m || ( echo "Can't access binfeats.m or getBinStumps.m."; exit 1 )



# Run Matlab script
rm -f nohup.out
nohup matlab -nodesktop -nosplash -nodisplay -nojvm -r binfeats </dev/null
# Check that at least one file was created:
ls data_obj_feats.b.txt || ( echo "Problem running matlab, file data_obj_feats.b.txt was not found. Check nohup.out"; exit 1 )


# Run Perl scripts
perl ../scripts/format_svm_seg.pl Segmentation_labeling.txt . 1 > log_format_svm_seg.pl.log
mkdir segments
perl ../scripts/createSegmentsFiles.pl . "$method" > log_createSegmentsFiles.pl.log
mkdir -p formatted/segments/$method
mv segments/* formatted/segments/$method
mkdir -p formatted/data/$method
mv [01]*txt formatted/data/$method

# Clean up
rm -r segments
