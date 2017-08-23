from __future__ import print_function
from __future__ import division
import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument("--indir", type=str, help="input dir")
parser.add_argument("--ofile", type=str, help="output file")
args = parser.parse_args()

indir = args.indir
ofile = args.ofile

if indir[-1] != '/':
    indir += '/'

data = pd.read_csv('../assgmt1/dev.txt', sep='\t', header=None)
data.columns = [0,1,2]
pat = re.compile(r'(\d*)\t(\d*)\t(.)\t(\w*)\t(\d.\d*)')

num_cor = 0
tot_num = 0
# fname_format = './eval/txt_dir2/{}.txt'
tuple_list = list()
# fname_format = './eval/txt_dup_dir2/{}.txt'
# fname_format = './eval/txt_swap_dir2/{}.txt'
fname_format = indir + '{}.txt'
for i in range(data.last_valid_index() + 1):
    guess = False
    ind, w_corr, w_wrong = data.loc[i]
    fname = fname_format.format(str(ind))
    with open(fname, 'r') as f:
        lines = f.read()
        patterns = pat.findall(lines)
    if len(patterns) == 0:
        continue
    if patterns[0][3] == w_corr:
        num_cor += 1
        guess = True
    tot_num += 1
    tuple_list.append((ind, w_corr, w_wrong, patterns[0][3], guess))
    if not guess:
        print(ind, w_corr, w_wrong, patterns[0][3], guess)
print(num_cor, tot_num, num_cor/tot_num)
str_format = '{} {} {}\n'
with open(ofile, 'w') as f:
    f.write(str_format.format(num_cor, tot_num, num_cor/tot_num))
