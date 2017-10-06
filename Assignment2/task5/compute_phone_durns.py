import argparse
from subprocess import call
import re
parser = argparse.ArgumentParser()
parser.add_argument('trdir', type=str, help="train dir")
args = parser.parse_args()
train_dir = args.trdir
if train_dir[-1] == '/':
    data_dir = '/'.join(train_dir.split('/')[:-2])
else:
    data_dir = '/'.join(train_dir.split('/')[:-1])
print(train_dir)
print(data_dir)
call(['./run1.sh', data_dir])

# Assuming all data processing till align step is done using run1.sh


pat = re.compile(r'Overall,\s(.*)\saccounts\sfor\s(.*)%\sof\sphone\soccurrences,\swith\sduration\s\(median, mean, 95-percentile\)\sis\s\((.*),(.*),(.*)\)\sframes.')

with open('./exp/mono_ali/log/analyze_alignments.log', 'r') as f:
    lines = f.read()
    phone_list = pat.findall(lines)

for p in phone_list:
    print(p[0], float(p[2]) * 0.01)
