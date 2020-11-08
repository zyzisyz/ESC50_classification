#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import numpy as np
import torch
import torchaudio
from torch.utils.data import Dataset
from scipy.io import wavfile
import librosa


class ESC50Dataset(Dataset):
	def __init__(self, csv_path="meta/esc50.csv", audio_dir="audio"):
		print("init ESC50Dataset...")
		df = pd.read_csv("./meta/esc50.csv")
		print(df)
		file_path = df.filename.values
		self.file_path = ["audio/"+x for x in file_path]
		self.labels = df.target.values

	def __len__(self):
		return len(self.labels)

	def __getitem__(self, idx):
		waveform, samplerate = librosa.load(self.file_path[idx])
		MFCC = librosa.feature.mfcc(y=waveform, sr=samplerate, n_mfcc=40).T
		MFCC = torch.from_numpy(MFCC.copy())
		MFCC = MFCC.unsqueeze(0)
		label = torch.tensor(self.labels[idx])
		return MFCC, label



