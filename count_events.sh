#!/bin/sh
NICE="nice -n 19"
base_dir1="$1"
base_dir2="$2"
base_dir3="$3"
base_dir4="$4"
which_file="$5"
file_stamp="$base_dir1$base_dir2$base_dir3$base_dir4"_"$which_file"

# check if file exists.
raw_file=/pear/share/www-uniq/v2006-2015.cf-preparation/knp/$base_dir1/$base_dir2/$base_dir3/$base_dir4/$base_dir1$base_dir2$base_dir3$base_dir4$which_file.knp.xz
if ! [ -f $raw_file ]
then
    echo "$raw_file not existed."
    exit
fi

# decompress.
knp_file=/data/huang/temp_$file_stamp.knp
n=0
until [ $n -ge 10000 ]
do
    xz -d $raw_file -c > $knp_file && break
    n=$[$n+1]
    sleep 5
done

# extract events from knp file.
output_file=/windroot/huang/EventCounts/$file_stamp.txt
result_file=/windroot/huang/EventCounts/"$file_stamp"_result.txt
process_file_script=/home/huang/work/EventCounts/process_knp_file.py
merge_script=/home/huang/work/EventCounts/merge.py
$NICE python $process_file_script -i $knp_file -o $output_file -s
$NICE sort -k2 $output_file -o $output_file
$NICE python $merge_script -t 2 -f $output_file -s > $result_file

# remove temp files.
rm -f $knp_file
rm -f $output_file
echo "$file_stamp done"
