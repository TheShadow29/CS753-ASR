from subprocess import call

call(['fstcompose', './dev_wrd/bin/134.fsa', './bin/E_bin.fst', 'tmp1.fst'])
call(['fstcompose', 'tmp1.fst', './dev_wrd/bin/140.fsa', 'tmp2.fst'])
# call(['fstshortestdistance', 'tmp2.fst'])
