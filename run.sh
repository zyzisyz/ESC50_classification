#!/bin/bash

python -u main.py \
	--epochs 20 \
	--batch-size 64 \
	--test-batch-size 150 \
	--num-workers 20 \
	--save-model \
	--log-interval 1 \
	--ckpt-path "ckpt/ckpt_3.pt" \
	--ckpt-save-dir ckpt

