#! /bin/bash

set -e      # Stop on errors
#set -x      # Print commands before they are run

c=$1
e=$2
i=$3
modelFile=$4
modelFolder=$5
suffix=$6
w=$7

cd fold$i
../../svm_python_learn --m svmstruct_mrf_act -c $c  -e $e -w $w --sf false --temporal true train$i.txt models/$modelFile >> logs/log.$suffix 2>> logs/err.learn.$suffix

sleep 2
../../svm_python_classify --m svmstruct_mrf_act --sf false --temporal true test$i.txt models/$modelFile pred/pred.$modelFile > pred/out.$modelFile 2>> logs/err.classify_test.$suffix
../../svm_python_classify --m svmstruct_mrf_act --sf false --temporal true cvtrain$i.txt models/$modelFile pred/cvtrain.pred.$modelFile > pred/cvtrain.out.$modelFile 2>> logs/err.classify_cv.$suffix
#../../../svm_python_classify --m svmstruct_mrf_act --sf false --temporal true train$i.txt models/$modelFile pred/train.pred.$modelFile > pred/train.out.$modelFile 2>> logs/err.classify_train.$suffix
cd - 
