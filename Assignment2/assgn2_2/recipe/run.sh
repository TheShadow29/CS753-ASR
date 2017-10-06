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
stage=2    # from which stage should this script start
corpus=./audio  # corpus containing speech,transcripts,pronunciation dictionary
nj=4        # number of parallel jobs to run during training
dev_nj=4    # number of parallel jobs to run during decoding
# the above two parameters are typically set to the number of cores on your machine
###############################################################

# The following command prepares the data/{train,dev} directories.
if [ $stage -le 0 ]; then
	local/prepare_data.sh $corpus || exit 1;
	local/prepare_lang.sh  || exit 1;
	local/prepare_lang_word.sh  || exit 1;
	utils/validate_lang.pl data/lang
fi

# Now make MFCC features.
# mfccdir should be some place with a largish disk where you
# want to store MFCC features.
mfccdir=mfcc

if [ $stage -le 0 ]; then
	for x in train dev; do
		steps/make_mfcc.sh --cmd "$train_cmd" --nj $nj \
						   data/$x exp/make_mfcc/$x $mfccdir || exit 1;
		steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x $mfccdir || exit 1;
	done
fi

# Monophone
if [ $stage -le 1 ]; then
	echo "Monophone training"
	steps/train_mono.sh  --nj $nj --cmd "$train_cmd" \
						 data/train data/lang exp/mono
	echo "Monophone training complete"

	echo "Decoding the dev set using monophone models."
	utils/mkgraph.sh data/lang exp/mono exp/mono/graph
	steps/decode.sh --nj $dev_nj --cmd "$decode_cmd" \
					exp/mono/graph data/dev exp/mono/decode_dev
	echo "Monophone decoding done."

	echo "Monophone training for Word Based"
	steps/train_mono.sh  --nj $nj --cmd "$train_cmd" \
						 data/train data/lang_word exp/word_based
	echo "Monophone training complete"

	echo "Decoding the dev set using Word Based HMM."
	utils/mkgraph.sh data/lang_word exp/word_based exp/word_based/graph
	steps/decode.sh --nj $dev_nj --cmd "$decode_cmd" \
					exp/word_based/graph data/dev exp/word_based/decode_dev
	echo "Monophone decoding done."

fi
# stage=11
# Triphone
if [ $stage -le 2 ]; then
	echo "Triphone training"
	steps/align_si.sh --nj $nj --cmd "$train_cmd" \
					  data/train data/lang exp/mono exp/mono_ali
	steps/train_deltas.sh --cmd "$train_cmd" \
						  5000 5000 data/train data/lang exp/mono_ali exp/tri1
	echo "Triphone training complete"

	echo "Decoding the dev set using triphone models."
	utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph
	steps/decode.sh --nj $dev_nj --cmd "$decode_cmd" \
					exp/tri1/graph data/dev exp/tri1/decode_dev
	echo "Triphone decoding done"
fi

if [ $stage -le 3 ]; then
	echo "Tri alignment"
	steps/align_si.sh --nj $nj --cmd "$train_cmd" \
					  data/train data/lang exp/tri1 exp/tri1_ali
	steps/train_deltas.sh --cmd "$train_cmd" \
						  2000 11000 data/train data/lang exp/tri1_ali exp/tri2a
fi

if [ $stage -le 4 ]; then
	echo "Decoding tri ali"
	utils/mkgraph.sh data/lang exp/tri2a exp/tri2a/graph
	steps/decode.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
					exp/tri2a/graph data/dev exp/tri2a/decode_dev
fi

if [ $stage -le 5 ]; then
	echo "Using LDA+MLTT"
	steps/train_lda_mllt.sh --cmd "$train_cmd" 2000 11000 \
							data/train data/lang exp/tri1_ali exp/tri2b || exit 1;
	utils/mkgraph.sh data/lang exp/tri2b exp/tri2b/graph
	steps/decode.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
					exp/tri2b/graph data/dev exp/tri2b/decode_dev
fi

if [ $stage -le 6 ]; then
	echo "MMI"
	steps/align_si.sh --nj $nj --cmd "$train_cmd" \
					  data/train data/lang exp/tri2b exp/tri2b_ali || exit 1;
	steps/make_denlats.sh --nj $nj --cmd "$train_cmd" \
						  data/train data/lang exp/tri2b exp/tri2b_denlats || exit 1;
	steps/train_mmi.sh data/train data/lang exp/tri2b_ali exp/tri2b_denlats exp/tri2b_mmi || exit 1;

	steps/decode.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
					exp/tri2b/graph data/dev exp/tri2b_mmi/decode_dev

	# steps/decode.sh --config conf/decode.config --iter 4 --nj $dev_nj --cmd "$decode_cmd" \
	#				exp/tri2b/graph data/dev exp/tri2b_mmi/decode_it4
	# steps/decode.sh --config conf/decode.config --iter 3 --nj $dev_nj --cmd "$decode_cmd" \
	#				exp/tri2b/graph data/dev exp/tri2b_mmi/decode_it3
	# steps/decode.sh --config conf/decode.config --iter 2 --nj $dev_nj --cmd "$decode_cmd" \
	#				exp/tri2b/graph data/dev exp/tri2b_mmi/decode_it5

fi

if [ $stage -le 7 ]; then
	echo "Boosted MMI"
	steps/train_mmi.sh --boost 0.05 data/train data/lang \
					   exp/tri2b_ali exp/tri2b_denlats exp/tri2b_mmi_b0.05 || exit 1;
	steps/decode.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
					exp/tri2b/graph data/dev exp/tri2b_mmi_b0.05/decode_dev

	# steps/decode.sh --config conf/decode.config --iter 4 --nj $dev_nj --cmd "$decode_cmd" \
	#				exp/tri2b/graph data/dev exp/tri2b_mmi_b0.05/decode_it4 || exit 1;
	# steps/decode.sh --config conf/decode.config --iter 3 --nj $dev_nj --cmd "$decode_cmd" \
	#				exp/tri2b/graph data/dev exp/tri2b_mmi_b0.05/decode_it3 || exit 1;
	# steps/decode.sh --config conf/decode.config --iter 5 --nj $dev_nj --cmd "$decode_cmd" \
	#				exp/tri2b/graph data/dev exp/tri2b_mmi_b0.05/decode_it5

fi

if [ $stage -le 8 ]; then
	echo "MPE"
	steps/train_mpe.sh data/train data/lang exp/tri2b_ali exp/tri2b_denlats exp/tri2b_mpe || exit 1;
	steps/decode.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
					exp/tri2b/graph data/dev exp/tri2b_mpe/decode_dev || exit 1;
fi

if [ $stage -le 9 ]; then
	echo "LDA+MLLT+SAT"
	steps/train_sat.sh 2000 11000 data/train data/lang exp/tri2b_ali exp/tri3b || exit 1;
	utils/mkgraph.sh data/lang exp/tri3b exp/tri3b/graph || exit 1;
	steps/decode_fmllr.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
						  exp/tri3b/graph data/dev exp/tri3b/decode || exit 1;
fi
if [ $stage -le 10 ]; then
	echo "MMI on top of LDA+MLLT+SAT"
	steps/align_fmllr.sh --nj $dev_nj --cmd "$train_cmd" --use-graphs true \
						 data/train data/lang exp/tri3b exp/tri3b_ali || exit 1;

	steps/make_denlats.sh --config conf/decode.config \
						  --nj $nj --cmd "$train_cmd" --transform-dir exp/tri3b_ali \
						  data/train data/lang exp/tri3b exp/tri3b_denlats || exit 1;

	steps/train_mmi.sh data/train data/lang exp/tri3b_ali exp/tri3b_denlats exp/tri3b_mmi || exit 1;

	steps/decode_fmllr.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
						  --alignment-model exp/tri3b/final.alimdl --adapt-model exp/tri3b/final.mdl \
						  exp/tri3b/graph data/dev exp/tri3b_mmi/decode || exit 1;

	steps/decode.sh --config conf/decode.config --nj $dev_nj --cmd "$decode_cmd" \
					--transform-dir exp/tri3b/decode  exp/tri3b/graph data/dev exp/tri3b_mmi/decode2 || exit 1;
fi



# steps/make_denlats.sh --nj 30 --sub-split 30 --cmd "$train_cmd" \
#   data/train data/lang exp/tri1_ali exp/tri1_denlats || exit 1;

# steps/train_mmi.sh --cmd "$train_cmd" --boost 0.1 \
#   data/train_ data/lang exp/tri1_ali exp/tri1_denlats \
#   exp/tri1_mmi  || exit 1;

wait;
# Computing the WERs on the development set
for x in exp/*/decode*; do [ -d $x ] && grep WER $x/wer_* | utils/best_wer.sh; done
