#!/bin/bash


#--ckpt-path "ckpt/ckpt_3.pt" 

python -u main.py \
	--epochs 50 \
	--batch-size 100 \
	--test-batch-size 150 \
	--num-workers 40 \
	--save-model \
	--log-interval 1 \
	--ckpt-save-dir ckpt

