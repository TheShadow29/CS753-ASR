isymb=$1
osymb=$2
text=$3
bin=$4
fstcompile --isymbols=$isymb --osymbols=$osymb $text $bin.fst
fstdraw --isymbols=$isymb --osymbols=$osymb $bin.fst $bin.dot
dot -Tps $bin.dot > $bin.ps
