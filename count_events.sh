#!/bin/bash
NICE="nice -n 19"
export LC_ALL=C

file_stamp="$1"
file_stamp_base=`basename $file_stamp`

config_file="$2"
source $config_file

# check if file exists.
raw_file="$raw_dir/$file_stamp$raw_postfix"
if ! [ -f $raw_file ]
then
    echo "$raw_file not existed."
    exit
fi

# decompress.
knp_file="$extract_tmp_dir/$file_stamp_base.knp"
n=0
until [ $n -ge 10000 ]
do
    xz -d $raw_file -c > $knp_file && break
    n=$[$n+1]
    sleep 5
done

# extract events from knp file.
extracted_tmp_fn="$extract_tmp_dir/$file_stamp_base.unsorted"
extracted_file="$extract_dir/$file_stamp.txt"
extract_sub_dir=`dirname $extracted_file`
mkdir -p $extract_sub_dir

process_knp_script="./process_knp_file.py"
merge_script="./merge.py"

COUNT_THRESHOLD=2
$NICE python $process_knp_script -i $knp_file -o $extracted_tmp_fn $extract_options
echo "extratced to $extracted_tmp_fn"

if $extract_sid;
then
    $NICE sort -k2,2 $extracted_tmp_fn -o $extracted_tmp_fn
    echo "sorted to $extracted_tmp_fn"
    $NICE python $merge_script -t $COUNT_THRESHOLD -f $extracted_tmp_fn -s > $extracted_file
else
    $NICE sort $extracted_tmp_fn | uniq -c | sed 's/^ *\([0-9]*\) /\1 /' > $extracted_file
fi
echo "merged to $extracted_file"

# remove temp files.
rm -f $knp_file
rm -f $extracted_tmp_fn
echo "$file_stamp_base done"

