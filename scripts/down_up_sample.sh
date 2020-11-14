#!/bin/bash

for file in `find ./data/train -name "*.wav"`
do
	for sample_rate in 16000 8000 32000
	do
		{
			tmp=${file%.*}_${sample_rate}_tmp.wav
			dst=${file%.*}_${sample_rate}.wav
			rm -rf $tmp
			rm -rf $dst
			sox $file -r ${sample_rate} $tmp
			sox $tmp -r 44100 $dst
			rm -rf $tmp
		}&
	done
done

wait
echo done

