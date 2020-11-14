#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import numpy as np
import librosa
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split 
import torch
import os

def load_file(csv_path="meta/esc50.csv", audio_dir="audio/"):
	df = pd.read_csv(csv_path)
	file_path = df.filename.values
	file_path = [audio_dir + x for x in file_path]
	labels = df.target.values
	return file_path, labels


if __name__ == "__main__":
	file_path, labels = load_file()
	train_path, test_path, train_label, test_label = train_test_split(file_path, labels, test_size=0.2, random_state=42, shuffle=True)
	for label in np.unique(labels):
		if not os.path.exists("./data/train/{}".format(label)):
			os.makedirs("./data/train/{}".format(label))
		if not os.path.exists("./data/test/{}".format(label)):
			os.makedirs("./data/test/{}".format(label))

	for idx in range(len(train_path)):
		file_name = train_path[idx].split("/")[-1].split(".")[0]
		waveform, samplerate = librosa.load(train_path[idx])
		MFCC = librosa.feature.mfcc(y=waveform, sr=samplerate, n_mfcc=40).T
		MFCC = torch.from_numpy(MFCC.copy())
		MFCC = MFCC.unsqueeze(0)
		torch.save(MFCC, "data/train/{}/{}.MFCC".format(train_label[idx], file_name))

	for idx in range(len(test_path)):
		file_name = test_path[idx].split("/")[-1].split(".")[0]
		waveform, samplerate = librosa.load(test_path[idx])
		MFCC = librosa.feature.mfcc(y=waveform, sr=samplerate, n_mfcc=40).T
		MFCC = torch.from_numpy(MFCC.copy())
		MFCC = MFCC.unsqueeze(0)
		torch.save(MFCC, "data/test/{}/{}.MFCC".format(test_label[idx], file_name))

