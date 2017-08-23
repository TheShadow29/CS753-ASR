from __future__ import print_function
from __future__ import division
import pandas as pd
import re

data = pd.read_csv('../assgmt1/dev.txt', sep='\t', header=None)
data.columns = [0,1,2]
pat = re.compile(r'(\d*)\t(\d*)\t(.)\t(.*)\t(\d.\d*)')

num_cor = 0
tot_num = 0
fname_format = './eval/txt_dir/{}.txt'
for i in range(data.last_valid_index() + 1):
    guess = False
    ind, w_corr, w_wrong = data.loc[i]
    fname = fname_format.format(str(ind))
    with open(fname, 'r') as f:
        lines = f.read()
        patterns = pat.findall(lines)


    if patterns[0][3] == w_corr:
        num_cor += 1
        guess = True
    tot_num += 1
    print(ind, w_corr, w_wrong, patterns[0][3], guess)
print(num_cor, tot_num, num_cor/tot_num)
