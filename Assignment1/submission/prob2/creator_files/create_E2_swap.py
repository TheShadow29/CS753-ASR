from __future__ import print_function
from __future__ import division
import pandas as pd
import string
# import pdb

data = pd.read_csv('../assgmt1/lets.vocab', sep='\t', header=None)
data.columns = [0,1]

str_format = '0 1 {} {} {}\n'
str_format2 = '{} {} {} {} {}\n'
str_to_write = ''

e_fst_file = open('E2_swap_text.fst', 'w')
ctr = 2
for l in data[0][1:]:
    # pdb.set_trace()
    alphabets = list(string.ascii_lowercase)
    alphabets.remove(l)
    # subs
    for alph in alphabets:
        str_to_write += str_format.format(l, alph, str(1))
    # del
    str_to_write += str_format.format(l, '-', str(1))
    # ins
    str_to_write += str_format.format('-', l, str(1))
    # self-loop
    str_to_write += str_format2.format(0, 0, l, l, 0)
    str_to_write += str_format2.format(1, 1, l, l, 0)
    # swap
    for alph in alphabets:
        str_to_write += str_format2.format(0, ctr, l, alph, 0)
        str_to_write += str_format2.format(ctr, 1, alph, l, 1)
        ctr += 1

str_to_write += '0\n'
str_to_write += '1\n'

e_fst_file.write(str_to_write)
e_fst_file.close()
