#!/bin/bash

echo format data dir
python -u scripts/format_data_dir.py

echo downsample and upsample
bash ./scripts/down_up_sample.sh

echo make MFCCs
