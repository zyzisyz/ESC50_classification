#!/bin/bash

for suffix in fbank mfcc _tmp.wav* _16000.wav* _32000.wav* _8000.wav* _gl.wav* _world* npy
do
	for file in `find ./data -name *$suffix`
	do
		rm -rf $file &
	done
done

wait
echo done
