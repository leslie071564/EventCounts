#!/bin/sh
NICE="nice -n 19"
file_loc="$1"

split_line=$(grep -m 1 -n " \[人名\]" $file_loc | cut -f1 -d :)
tmp_file=$file_loc.tmp
$NICE tail -n +$split_line $file_loc > $tmp_file
mv -f $tmp_file $file_loc

echo $file_loc cleaned
