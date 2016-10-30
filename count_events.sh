#!/bin/sh
NICE="nice -n 19"
base_dir1="$1"
base_dir2="$2"
base_dir3="$3"
base_dir4="$4"
which_file="$5"

# read from config file
config_file=./setting.ini
read_ini_script=./read_ini.sh
source $read_ini_script
read_ini $config_file

raw_dir=$INI__Data_Directory__raw_dir
knp_tmp_dir=$INI__Data_Directory__knp_tmp_dir
result_dir=$INI__Data_Directory__result_dir
process_file_script=$INI__Scripts__process_knp_script
merge_script=$INI__Scripts__merge_script
echo $raw_dir
echo $knp_tmp_dir
echo $result_dir
echo $process_file_script
echo $merge_script

# check if file exists.
file_stamp="$base_dir1$base_dir2$base_dir3$base_dir4"_"$which_file"
raw_file=$raw_dir/$base_dir1/$base_dir2/$base_dir3/$base_dir4/$base_dir1$base_dir2$base_dir3$base_dir4$which_file.knp.xz
if ! [ -f $raw_file ]
then
    echo "$raw_file not existed."
    exit
fi

# decompress.
knp_file=$knp_temp_dir/temp_$file_stamp.knp
n=0
until [ $n -ge 10000 ]
do
    xz -d $raw_file -c > $knp_file && break
    n=$[$n+1]
    sleep 5
done

# extract events from knp file.
output_file=$result_dir/$file_stamp.txt
result_file=$result_dir/"$file_stamp"_result.txt
$NICE python $process_file_script -i $knp_file -o $output_file -s
$NICE LC_ALL=C sort -k2 $output_file -o $output_file
$NICE python $merge_script -t 2 -f $output_file -s > $result_file

# remove temp files.
rm -f $knp_file
rm -f $output_file
echo "$file_stamp done"
