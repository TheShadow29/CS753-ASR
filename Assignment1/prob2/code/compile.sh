isymb=$1
osymb=$2
text=$3
bin=$4
opt="_opt"
# bin_opt=$bin _opt
fstcompile --isymbols=$isymb --osymbols=$osymb $text $bin.fst
fstrmepsilon $bin.fst | fstdeterminize | fstminimize > $bin$opt.fst
binopt=$bin$opt
fstdraw --isymbols=$isymb --osymbols=$osymb $binopt.fst $binopt.dot
dot -Tpng $binopt.dot > $binopt.png
