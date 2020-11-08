#!/bin/bash

git clone https://gitee.com/zyziszy/ESC-50.git

rm -rf ./audio
rm -rf ./meta

ln -s ESC-50/audio/ ./audio
ln -s ESC-50/meta/ ./meta

