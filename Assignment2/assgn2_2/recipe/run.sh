#!/bin/bash
# Apache 2.0

# This script prepares data and trains + decodes an ASR system.

# initialization PATH
. ./path.sh  || die "path.sh expected";
# initialization commands
. ./cmd.sh
. ./utils/parse_options.sh
set -e -o pipefail

###############################################################
#                   Configuring the ASR pipeline
###############################################################
stage=0    # from which stage should this script start
corpus=./corpus  # corpus containing speech,transcripts,pronunciation dictionary
nj=4        # number of parallel jobs to run during training
dev_nj=4    # number of parallel jobs to run during decoding 
# the above two parameters are typically set to the number of cores on your machine
###############################################################

# The following command prepares the data/{train,dev} directories.
local/prepare_data.sh $corpus || exit 1;
local/prepare_lang.sh  || exit 1;
utils/validate_lang.pl data/lang/

# Now make MFCC features.
# mfccdir should be some place with a largish disk where you
# want to store MFCC features.
mfccdir=mfcc
for x in train dev; do
  steps/make_mfcc.sh --cmd "$train_cmd" --nj $nj \
    data/$x exp/make_mfcc/$x $mfccdir || exit 1;
  steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x $mfccdir || exit 1;
done

# Monophone
echo "Monophone training"
steps/train_mono.sh  --nj $nj --cmd "$train_cmd" \
  data/train data/lang exp/mono
echo "Monophone training complete"

echo "Decoding the dev set using monophone models."
utils/mkgraph.sh data/lang exp/mono exp/mono/graph
steps/decode.sh --nj $dev_nj --cmd "$decode_cmd" \
  exp/mono/graph data/dev exp/mono/decode_dev
echo "Monophone decoding done."

# Triphone
echo "Triphone training"
steps/align_si.sh --nj $nj --cmd "$train_cmd" \
  data/train data/lang exp/mono exp/mono_ali
steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" \
  300 3000 data/train data/lang exp/mono_ali exp/tri1
echo "Triphone training complete"

echo "Decoding the dev set using triphone models."
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph
steps/decode.sh --nj $dev_nj --cmd "$decode_cmd" \
  exp/tri1/graph data/dev exp/tri1/decode_dev

wait;
# Computing the WERs on the development set
for x in exp/*/decode*; do [ -d $x ] && grep WER $x/wer_* | utils/best_wer.sh; done
