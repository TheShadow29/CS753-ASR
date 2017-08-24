from __future__ import print_function
from __future__ import division
import pandas as pd
import numpy as np

data = pd.read_csv('../assgmt1/wordcounts.txt', sep=' ', header=None)
data.columns = [0, 1]

arr = np.array(data[1])
tot_count = arr.sum()
arr1 = arr / tot_count
neg_log_prob_arr = -np.log10(arr1) / 2

g_fst_file = open('G_text.fst', 'w')
str_to_write = ''
str_format = '0 0 {} {} {}\n'

str_to_write += '0\n'

for ind, w in enumerate(data[0][:]):
    str_to_write += str_format.format(w, w, neg_log_prob_arr[ind])

print(str_to_write)
g_fst_file.write(str_to_write)
g_fst_file.close()
