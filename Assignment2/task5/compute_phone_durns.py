# import argparse
# from subprocess import call

# parser = argparse.ArgumentParser()
# parser.add_argument('trdir', type=str, help="train dir")
# args = parser.parse_args()
# train_dir = args.trdir
# print(train_dir)
# # if
# # Assuming kaldi root is set properly
# nj = '4'
# train_cmd = 'run.pl'
# call(['steps/make_mfcc.sh',
# '--nj', nj, '--cmd', train_cmd, train_dir, 'exp/make_mfcc/train', 'mfcc'])
# call(['steps/compute_cmvn_stats.sh', train_dir, 'exp/make_mfcc/train', 'mfcc'])
# Assuming all data processing till align step is done using run1.sh

import re
pat = re.compile(r'Overall,\s(.*)\saccounts\sfor\s(.*)%\sof\sphone\soccurrences,\swith\sduration\s\(median, mean, 95-percentile\)\sis\s\((.*),(.*),(.*)\)\sframes.')

with open('./exp/mono_ali/log/analyze_alignments.log', 'r') as f:
    lines = f.read()
    phone_list = pat.findall(lines)

for p in phone_list:
    print(p[0], float(p[2]) * 0.01)
