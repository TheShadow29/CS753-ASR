from __future__ import print_function
from __future__ import  division
import subprocess
from subprocess import call
import argparse
import pandas as pd
import os
import re
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('dev', type=str, help='devtxt')
parser.add_argument("--Mdir", type=str, help="dev word dir")
parser.add_argument("--E", type=str, help="E.fst location")
parser.add_argument("--T", type=str, help="T.fst location")
parser.add_argument("--G", type=str, help="G.fst location")
parser.add_argument("--odir", type=str, help="outdir for txt files")
args = parser.parse_args()

mdir = args.Mdir
if mdir[-1] != '/':
    mdir += '/'
e_fst_file = args.E
t_fst_file = args.T
g_fst_file = args.G
dev_txt_fname = args.dev
pat = re.compile(r'(\d*)\t(\d*)\t\w\t(.*)\t(\d.\d*)')
# print(mdir, e_fst_file, t_fst_file, g_fst_file)
data = pd.read_csv(dev_txt_fname, sep='\t', header=None)
data.columns = [0, 1, 2]

out_dir = args.odir
if out_dir[-1] != '/':
    out_dir += '/'
dot_dir = out_dir + '/dot/'
txt_dir = out_dir + '/txt_direc/'
# txt_dir = out_dir + '/txt_dup_dir2/'
# txt_dir = out_dir + '/txt_swap_dir2/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
if not os.path.exists(dot_dir):
    os.makedirs(dot_dir)
if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)


t_inv_file = out_dir + 'T_inverse.fst'
t_inv_opt_file = out_dir + 'T_inverse_opt.fst'

# NEED TO UNCOMMENT BEFORE SUBMITTING
call(['fstinvert', t_fst_file, t_inv_file])
cmd = 'fstrmepsilon ' + t_inv_file + ' | fstdeterminize | fstminimize > ' + t_inv_opt_file
output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p1 = output.communicate()[0]
call(['fstarcsort', t_inv_opt_file, t_inv_opt_file])


tmp1_fst = out_dir + 'tmp1.fst'
tmp2_fst = out_dir + 'tmp2.fst'
tmp3_fst = out_dir + 'tmp3.fst'
tmp4_fst = out_dir + 'tmp4.fst'

call(['fstcompose', t_inv_opt_file, g_fst_file, tmp1_fst])
call(['fstarcsort', tmp1_fst, tmp1_fst])
call(['fstcompose', e_fst_file, tmp1_fst, tmp2_fst])
call(['fstarcsort', tmp2_fst, tmp2_fst])

for i in range(data.last_valid_index() + 1):
# for i in range(1):
    ind, w_correct, w_wrong = data.loc[i]

    call(['fstcompose', mdir + str(ind) + '.fsa', tmp2_fst, tmp3_fst])
    call(['fstarcsort', tmp3_fst, tmp3_fst])
    call(['fstshortestpath', '--nshortest=' + str(1), tmp3_fst, tmp4_fst])
    txt_fname = txt_dir + str(ind) + '.txt'
    call(['fstprint', tmp4_fst, txt_fname])
    print('Iter', i, 'ind', ind)
# f = open(txt_fname, 'r')

# lines = f.read()
# p_list = pat.findall(lines)
