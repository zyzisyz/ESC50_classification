#!/bin/bash

stage=5
echo This is stage: $stage

nj=60

data_dir=data
type=fbank

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
	for i in `seq 0 49`
	do
		for file in `find ./data/train/$i -name "*.wav"`
		do
			{
				dst=${file%.*}_gl.wav
				rm -rf $dst
				echo $dst
				python scripts/griffin_lim_aug.py \
					--src_wav $file \
					--dst_wav $dst
			}&
		done
		wait
	done
	wait
fi


if [ $stage -eq 4 ];then
	echo world aug
	for i in `seq 0 49`
	do
		for file in `find ./data/train/$i -name "*.wav"`
		do
			{
				dst=${file%.*}_world.wav
				rm -rf $dst
				echo $dst
				python scripts/world_aug.py \
					--src_wav $file \
					--dst_wav $dst
			}&
		done
		wait
	done
	wait
fi


if [ $stage -eq 5 ];then
	echo make Fbanks

	echo prepare $data_dir...
	rm -rf ark/sdata
	mkdir -p ark/sdata

	# make data list
	wav_scp=ark/data_list; [[ -f "$wav_scp" ]] && rm $wav_scp
	for wav in `find -L ${data_dir} -name "*.wav"`; do
		echo ${wav%.*} $wav >> $wav_scp
	done

	split_scps=""
	for n in $(seq $nj); do
		split_scps="$split_scps ark/sdata/$n"
	done
	utils/split_scp.pl $wav_scp $split_scps || exit 1;
	echo $data_dir done!

	echo compute $type
	rm -rf ark/$type
	mkdir -p ark/$type

	utils/run.pl JOB=1:$nj ark/sdata/log/JOB.log \
		compute-${type}-feats --config="conf/${type}.conf" scp:ark/sdata/JOB ark:- \| \
		apply-cmvn-sliding --norm-vars=false --center=false --cmn-window=498 ark:- ark:ark/${type}/JOB.ark \
		|| exit 1;


	echo make $type
	utils/run.pl JOB=1:$nj ark/sdata/log/JOB.log \
		python scripts/ark2pt.py \
		--ark_path="ark/${type}/JOB.ark" \
		--suffix="${type}" \
		--min_len=0
	rm -rf ark
fi

