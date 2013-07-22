#! /bin/bash

for i in `seq 1 4`
do
    mkdir fold$i

#  rm -rf fold$i/*

    mkdir fold$i/logs
    mkdir fold$i/pred
    mkdir fold$i/imodels
    mkdir fold$i/models
done

cat fold1.txt fold2.txt fold3.txt  > fold4/train4.txt
cat fold1.txt fold3.txt fold4.txt  > fold2/train2.txt
cat fold3.txt fold2.txt fold4.txt  > fold1/train1.txt
cat fold1.txt fold2.txt fold4.txt  > fold3/train3.txt

cat cvfold1.txt cvfold2.txt cvfold3.txt  > fold4/cvtrain4.txt
cat cvfold1.txt cvfold3.txt cvfold4.txt  > fold2/cvtrain2.txt
cat cvfold3.txt cvfold2.txt cvfold4.txt  > fold1/cvtrain1.txt
cat cvfold1.txt cvfold2.txt cvfold4.txt  > fold3/cvtrain3.txt

cat cvfold4.txt fold4.txt  > fold4/test4.txt
cat cvfold3.txt fold3.txt  > fold3/test3.txt
cat cvfold2.txt fold2.txt  > fold2/test2.txt
cat cvfold1.txt fold1.txt  > fold1/test1.txt

