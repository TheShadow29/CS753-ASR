from __future__ import print_function
from __future__ import division
import argparse
import os
import pandas as pd
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('fil', metavar='f', type=str)
parser.add_argument("--odir", type=str, help="output dir")
parser.add_argument("--vocab", type=str, help="letter vocab file")

args = parser.parse_args()

# print(args.file, args.odir, args.vocab)
out_dir = args.odir
dev_file = args.fil
vocab_file = args.vocab

if out_dir[-1] != '/':
    out_dir += '/'

# out_txt_dir = out_dir + 'txt/'
out_bin_dir = out_dir + 'bin/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
# if not os.path.exists(out_txt_dir):
#     os.makedirs(out_txt_dir)
if not os.path.exists(out_bin_dir):
    os.makedirs(out_bin_dir)




data = pd.read_csv(dev_file, sep ='\t', header=None)
data.columns = [0,1,2]

str_format = '{} {} {}\n'

for ind, w in enumerate(data[2]):
    ctr = 0
    str_to_write = ''
    for l in w:
        str_to_write += str_format.format(str(ctr), str(ctr+1), l)
        ctr += 1
    str_to_write += str(ctr)
    fid = str(data[0][ind])
    fname = fid + '.fsa.txt'
    full_fname = out_dir + fname
    with open(full_fname, 'w') as f:
        f.write(str_to_write)

    call(['fstcompile','--acceptor','-isymbols=' + vocab_file, full_fname, out_bin_dir + fid + '.fsa'])
