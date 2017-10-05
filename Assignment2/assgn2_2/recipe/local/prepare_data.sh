#!/bin/bash

# Copyright 2012  Johns Hopkins University (Author: Daniel Povey)
# Apache 2.0.

if [ $# -ne 1 ]; then
   echo "Argument should be the corpus directory, see ../run.sh for example."
   exit 1;
fi

corpus=$1

for x in train dev; do
  mkdir -p data/$x
  # get wav.scp
  cat $corpus/$x.txt | while read l
  do
    SPK_ID=$(echo "$l" | cut -d'/' -f 2 | cut -d'.' -f 1)
    echo "$SPK_ID $corpus/audio/$l"
  done > data/$x/wav.scp

  # Now get the "text" file that says what the transcription is.
  cat $corpus/$x.txt | while read l
  do
    SPK_ID=$(echo "$l" | cut -d'/' -f 2 | cut -d'.' -f 1)
    TEXT=$(echo "$l" | cut -d'/' -f 1)
    echo "$SPK_ID $TEXT"
  done > data/$x/text

  # now get the "utt2spk" file that says, for each utterance, the speaker name.  
  cat $corpus/$x.txt | while read l
  do
    SPK_ID=$(echo "$l" | cut -d'/' -f 2 | cut -d'.' -f 1)
    echo "$SPK_ID $SPK_ID"
  done > data/$x/utt2spk

  # create the file that maps from speaker to utterance-list.
  # utils/utt2spk_to_spk2utt.pl <data/$x/utt2spk >data/$x/spk2utt
  utils/fix_data_dir.sh data/$x
done

echo "Data preparation succeeded"
