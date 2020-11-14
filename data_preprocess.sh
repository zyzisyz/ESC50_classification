#!/bin/bash

stage=1
echo This is stage: $stage

if [ stage -eq 1 ];then
	echo format data dir
	python -u scripts/format_data_dir.py
fi

if [ stage -eq 2 ];then
	echo downsample and upsample aug
	bash ./scripts/down_up_sample.sh
fi

if [ stage -eq 3 ];then
	echo griff lim aug
fi

if [ stage -eq 4 ];then
	echo make MFCCs
fi

