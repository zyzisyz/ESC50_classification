#!/usr/bin/env python
# coding=utf-8

import librosa
import numpy as np
import soundfile as sf
import argparse
import pyworld as pw

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--src_wav', type=str, help='source wav file')
	parser.add_argument('--dst_wav', type=str, help='source wav file')
	args = parser.parse_args()

	y, sr = sf.read(args.src_wav)
	_f0, t = pw.dio(y, sr)    # raw pitch extractor
	f0 = pw.stonemask(y, _f0, t, sr)  # pitch refinement
	sp = pw.cheaptrick(y, f0, t, sr)  # extract smoothed spectrogram
	ap = pw.d4c(y, f0, t, sr)         # extract aperiodicity
	y_inv = pw.synthesize(f0, sp, ap, sr) # synthesize an utterance using the parameters

	len_diff = len(y)-len(y_inv)
	if len_diff > 0:
		y_inv = np.hstack((y_inv, y[-len_diff:]))
	if len_diff < 0:
		y_inv = y_inv[:len_diff]
	assert(len(y_inv) == len(y))

	sf.write(args.dst_wav, y_inv, sr, subtype='PCM_16')


