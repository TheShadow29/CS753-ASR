from __future__ import print_function

word_file = open('../assgmt1/words.vocab')
# letter_file = open('../assgmt1/lets.vocab')

words = word_file.readlines()

t_fst_file = open('T_text.fst', 'w')
str_to_write = ''
str_format = '{} {} {} {}\n'
str_final_state_format = '{}\n'
ctr = 0
for w in words[:]:
    w1 = w.split('\t')
    w1[-1] = w1[-1].split('\n')[0]
    curr_word = w1[0]
    str_to_write += str_format.format('0', str(ctr+1), str(curr_word), str(curr_word[0]))
    for l in curr_word[1:]:
        ctr += 1
        str_to_write += str_format.format(str(ctr), str(ctr+1), '-', l)
    ctr += 1
    str_to_write += str_final_state_format.format(str(ctr))

print(str_to_write)
t_fst_file.write(str_to_write)
t_fst_file.close()
