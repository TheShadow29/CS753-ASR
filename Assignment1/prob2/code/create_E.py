from __future__ import print_function
from __future__ import division
import pandas as pd
import string

data = pd.read_csv('../assgmt1/lets.vocab', sep='\t', header=None)
data.columns = [0,1]

str_format = '{} {} {} {} {}\n'
str_to_write = ''

e_fst_file = open('E_text.fst', 'w')

zero = '0'
one = '0'



str_to_write += '0\n'           #
# str_to_write += '1\n'

for l in data[0][1:4]:
    alphabets = list(string.ascii_lowercase)
    alphabets.remove(l)
    #substitution
    for alph in alphabets:
        str_to_write += str_format.format(zero, one, l, alph, one)
    #insertion
    str_to_write += str_format.format(zero, one, '-', l, one)
    #deletion
    str_to_write += str_format.format(zero, one, l, '-', one)
    #self-loop
    str_to_write += str_format.format(zero, zero, l, l, zero)

e_fst_file.write(str_to_write)
e_fst_file.close()
