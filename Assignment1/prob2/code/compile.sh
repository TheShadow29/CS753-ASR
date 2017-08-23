isymb=$1
osymb=$2
text=$3
bin=$4
opt="_opt"
# bin_opt=$bin _opt
binopt=$bin$opt
bin_dir='./bin/'
dot_dir='./dot/'
fstcompile --isymbols=$isymb --osymbols=$osymb --keep_isymbols --keep_osymbols $text $bin_dir$bin.fst
# fstrmepsilon $bin_dir$bin.fst | fstdeterminize | fstminimize > $bin_dir$binopt.fst
# fstdraw --isymbols=$isymb --osymbols=$osymb $bin_dir$binopt.fst $dot_dir$binopt.dot
# fstdraw $bin_dir$bin.fst $dot_dir$binopt.dot
# dot -Tpng $dot_dir$binopt.dot > $dot_dir$binopt.png
# fstdraw $bin_dir$bin.fst | dot -Tpng > $dot_dir$bin.png
