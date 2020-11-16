#!/usr/bin/env python
# coding=utf-8

import os
import pandas as pd
import numpy as np
import torch
import torchaudio
from torch.utils.data import Dataset
import librosa
from sklearn.utils import shuffle


class ESC50Dataset(Dataset):
	def __init__(self, csv_path="meta/esc50.csv", audio_dir="audio"):
		print("init ESC50Dataset...")
		df = pd.read_csv("./meta/esc50.csv")
		print(df)
		file_path = df.filename.values
		file_path = ["audio/"+x for x in file_path]
		labels = df.target.values
		self.file_path, self.labels = shuffle(file_path, labels)

	def __len__(self):
		return len(self.labels)

	def __getitem__(self, idx):
		waveform, samplerate = librosa.load(self.file_path[idx])
		MFCC = librosa.feature.melspectrogram(y=waveform, sr=samplerate, center=False).T
		MFCC = torch.from_numpy(MFCC.copy())
		MFCC = MFCC.unsqueeze(0)
		label = torch.tensor(self.labels[idx])
		return MFCC, label


class ESC50_Dataset(Dataset):
	def __init__(self, audio_dir="data/train", extension="fbank"):
		print("init {}...".format(audio_dir))
		self.Seqs, _ = findAllSeqs(audio_dir, extension=extension)

	def __len__(self):
		return len(self.Seqs)

	def __getitem__(self, idx):
		Seq = self.Seqs[idx]
		(label, path) = Seq
		feature = torch.load(path)
		feature = torch.from_numpy(feature.copy())
		feature = feature.unsqueeze(0)
		return feature, label


def findAllSeqs(dirName, extension='.wav'):
    r"""
        find all wav sequence in $dirName
    The speaker labels must be organized the following way
    \dirName
        \speaker_label
            \..
                ...
                seqName.extension
    """
    assert os.path.exists(dirName)

    if dirName[-1] != os.sep:
        dirName += os.sep

    prefixSize = len(dirName)
    speakersTarget = {}
    outSeqPaths = []
    outSpeakers_label = []
    outSpeakers_str = []

    print("finding all seq...")
    for root, dirs, filenames in os.walk(dirName, followlinks=True):
        filtered_files = [f for f in filenames if f.endswith(extension)]
        if len(filtered_files) > 0:
            speakerStr = (os.sep).join(
                root[prefixSize:].split(os.sep)[:1])
            if speakerStr not in speakersTarget:
                speakersTarget[speakerStr] = len(speakersTarget)
            speaker = speakersTarget[speakerStr]
            for filename in filtered_files:
                full_path = os.path.join(root, filename)
                outSeqPaths.append((speaker, full_path))
                outSpeakers_label.append(speaker)
                outSpeakers_str.append(speakerStr)
    return outSeqPaths, outSpeakers_label

