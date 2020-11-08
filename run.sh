#!/bin/bash

python -u main.py \
	--epochs 10 \
	--batch-size 64 \
	--test-batch-size 150 \
	--num-workers 20 \
	--log-interval 1

