#!/bin/bash

stage=3
echo This is stage: $stage

if [ $stage -eq 1 ];then
	echo format data dir
	rm -rf data
	python -u scripts/format_data_dir.py
fi

if [ $stage -eq 2 ];then
	echo downsample and upsample aug
	bash ./scripts/down_up_sample.sh
fi

if [ $stage -eq 3 ];then
	echo griff lim aug
	for file in `find ./data/train -name "*.wav"`
	do
		dst=${file%.*}_gl.wav
		rm -rf $dst
		echo $dst
		python scripts/griffin_lim_aug.py \
			--src_wav $file \
			--dst_wav $dst
	done
	wait
fi

if [ $stage -eq 4 ];then
	echo make MFCCs
fi

