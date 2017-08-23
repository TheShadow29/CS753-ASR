#!/usr/bin/env python
from subprocess import call
import argparse

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
out_dir = './evalF/'
call(['python', 'evaluator.py', '--Mdir='+ mdir, '--E=' + e_fst_file, '--T=' + t_fst_file, '--G=' + g_fst_file, '--odir='+out_dir])
call(['python', 'evaluate_accuracy.py', '--indir='+ out_dir + 'txt_direc/', '--ofile='+'acc1.txt'])
