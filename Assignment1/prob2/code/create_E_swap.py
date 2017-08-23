from __future__ import print_function
from __future__ import division
import pandas as pd
import string
# import pdb

data = pd.read_csv('../assgmt1/lets.vocab', sep='\t', header=None)
data.columns = [0,1]

str_format = '0 0 {} {} {}\n'
str2_format = '{} {} {} {} {}\n'
str_to_write = ''

e_fst_file = open('E_dup_text.fst', 'w')

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
    str_to_write += str_format.format(l, l, str(0))
    # swapping
    for alph in alphabets:
        str_to_write += str2_format.format()



str_to_write += '0\n'


e_fst_file.write(str_to_write)
e_fst_file.close()
