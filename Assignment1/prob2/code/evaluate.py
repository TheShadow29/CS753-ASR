from __future__ import print_function
from __future__ import  division
from subprocess import call
import argparse
import pandas as pd
import os

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

# print(mdir, e_fst_file, t_fst_file, g_fst_file)
data = pd.read_csv('../assgmt1/dev.txt', sep='\t', header=None)
data.columns = [0, 1, 2]

out_dir = './eval/'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

t_inv_file = out_dir + 'T_inverse.fst'
call(['fstinvert', t_fst_file, t_inv_file])

ind, w_correct, w_wrong = data.loc[5]

tmp1_fst = out_dir + 'tmp1.fst'
tmp11_fst = out_dir + 'tmp11.fst'
tmp2_fst = out_dir + 'tmp2.fst'
tmp3_fst = out_dir + 'tmp3.fst'
call(['fstcompose', mdir + str(ind) + '.fsa', e_fst_file, tmp1_fst])
# print('compose 1 done')
# call(['fstarcsort', tmp1_fst, tmp11_fst])
# print('Arc sort done')
# call(['fstcompose', tmp11_fst, t_inv_file, tmp2_fst])
# call(['fstcompose', tmp1_fst, t_inv_file, tmp2_fst])
# print('compose 2 done')
# call(['fstcompose', tmp2_fst, g_fst_file, tmp3_fst])
# print('compose 3 done')
# call(['fstcompose', t_inv_file, g_fst_file, tmp11_fst])
# print('C2 done')
# call(['fstarcsort', tmp1_fst, tmp1_fst])
# call(['fstarcsort', tmp11_fst, tmp11_fst])
# call(['fstcompose', tmp1_fst, tmp11_fst, tmp2_fst])
print('C1')
call(['fstarcsort', tmp1_fst, tmp1_fst])
print('A1')
call(['fstcompose', tmp1_fst, t_inv_file, tmp2_fst])
print('C2')
call(['fstarcsort', tmp2_fst, tmp2_fst])
print('A2')
call(['fstcompose', tmp2_fst, g_fst_file, tmp3_fst])
print('C3')
call(['fstarcsort', tmp3_fst, tmp3_fst])
print('A3')
print('All done')
