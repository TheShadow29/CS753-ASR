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
parser.add_argument("--Mdir", type=str, help="dev word dir")
parser.add_argument("--E", type=str, help="E.fst location")
parser.add_argument("--T", type=str, help="T.fst location")
parser.add_argument("--G", type=str, help="G.fst location")

args = parser.parse_args()

mdir = args.Mdir
e_fst_file = args.E
t_fst_file = args.T
g_fst_file = args.G
pat = re.compile(r'(\d*)\t(\d*)\t\w\t(.*)\t(\d.\d*)')
# print(mdir, e_fst_file, t_fst_file, g_fst_file)
data = pd.read_csv('../assgmt1/dev.txt', sep='\t', header=None)
data.columns = [0, 1, 2]

out_dir = './eval/'
dot_dir = out_dir + '/dot/'
txt_dir = out_dir + '/txt_dir/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
if not os.path.exists(dot_dir):
    os.makedirs(dot_dir)
if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

t_inv_file = out_dir + 'T_inverse.fst'
t_inv_opt_file = out_dir + 'T_inverse_opt.fst'

# NEED TO UNCOMMENT BEFORE SUBMITTING
# call(['fstinvert', t_fst_file, t_inv_file])
# cmd = 'fstrmepsilon ' + t_inv_file + ' | fstdeterminize | fstminimize > ' + t_inv_opt_file
# output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# p1 = output.communicate()[0]
# call(['fstarcsort', t_inv_opt_file, t_inv_opt_file])


tmp1_fst = out_dir + 'tmp1.fst'
tmp2_fst = out_dir + 'tmp2.fst'
tmp3_fst = out_dir + 'tmp3.fst'
tmp4_fst = out_dir + 'tmp4.fst'

for i in range(data.last_valid_index() + 1):
    ind, w_correct, w_wrong = data.loc[i]

    call(['fstcompose', mdir + str(ind) + '.fsa', e_fst_file, tmp1_fst])
    call(['fstarcsort', tmp1_fst, tmp1_fst])
    # call(['fstcompose', tmp1_fst, t_inv_opt_file, tmp2_fst])
    # call(['fstarcsort', tmp2_fst, tmp2_fst])
    # call(['fstcompose', tmp2_fst, g_fst_file, tmp3_fst])
    # call(['fstshortestpath', '--nshortest=' + str(2), tmp3_fst, tmp4_fst])
    call(['fstcompose', t_inv_opt_file, g_fst_file, tmp2_fst])
    call(['fstarcsort', tmp2_fst, tmp2_fst])
    call(['fstcompose', tmp1_fst, tmp2_fst, tmp3_fst])
    call(['fstshortestpath', '--nshortest=' + str(2), tmp3_fst, tmp4_fst])
    txt_fname = txt_dir + str(ind) + '.txt'
    call(['fstprint', tmp4_fst, txt_fname])
    print('Iter', i, 'ind', ind)
# f = open(txt_fname, 'r')

# lines = f.read()
# p_list = pat.findall(lines)
