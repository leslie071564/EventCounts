#!/bin/bash
NICE="nice -n 19"
export LC_ALL=C

DATE=$(date +"%Y%m%d")

### set config file by curent date.

config_file_tmp=./setting.ini
config_template=./setting_template.ini
cp $config_template $config_file_tmp
sed -i -e "s/#USER/$USER/g" $config_file_tmp 
sed -i -e "s/#DATE/$DATE/g" $config_file_tmp 

# mkdir.
read_ini_script=./read_ini.sh
source $read_ini_script
read_ini $config_file_tmp

exp_dir=$INI__Data_Directory__exp_dir
result_dir=$INI__Data_Directory__result_dir
merge_dir=$INI__Data_Directory__merge_dir
event_sid_cdbdir=$INI__Data_Directory__event_sid_cdbdir
event_count_cdbdir=$INI__Data_Directory__event_count_cdbdir
mkdir -p $result_dir $merge_dir $event_sid_cdbdir $event_count_cdbdir

knp_tmp_dir=$INI__Data_Directory__knp_tmp_dir
sort_tmp_dir=$INI__Data_Directory__sort_tmp_dir
gxpc e mkdir -p $knp_tmp_dir $sort_tmp_dir 

event_count_cdb=$INI__DataBase__event_count_cdb
event_sid_cdb=$INI__DataBase__event_sid_cdb

config_file=$INI__Scripts__config_file
mv $config_file_tmp $config_file 
echo config file: $config_file

###Extract events from files:
python print_task.py --event_extract_task_file event_extract.task --config_file $config_file
gxpc js -a work_file=event_extract.task -a cpu_factor=0.5
rm -f event_extract.task
echo all events extracted.

###Merge event files:
python print_task.py --merge_task_file merge_folder.task --config_file $config_file 
gxpc js -a work_file=merge_folder.task -a cpu_factor=0.5
echo event files merged for all folders.

python print_task.py --merge_group_task_file merge_group.task --config_file $config_file
gxpc js -a work_file=merge_group.task -a cpu_factor=0.5
rm -f merge_folder.task merge_group.task
echo event folders merged

tmp_dir=/data/$USER
all_event_file=$tmp_dir/all_sorted_$DATE.txt
tmp_file=$tmp_dir/tmp.txt
sort --parallel=10 --temporary-directory=$sort_tmp_dir -k2 $merge_dir/*_result_group.txt > $tmp_file
python ./merge.py -f $tmp_file -s > $all_event_file
echo all events merged at $all_event_file

### Build event-cdbs:
python build_event_db.py -i $all_event_file -c $event_count_cdb
echo event-count cdb database built at $event_count_cdbdir 
python build_event_db.py -i $all_event_file -s $event_sid_cdb
echo event-sid cdb database built at $event_sid_cdbdir 

### Get event counts file:
all_event_sorted=$exp_dir/all_events_counts_sorted.txt
cut -d' ' -f1,2 $all_event_file > $all_event_sorted 
sort --parallel=10 --temporary-directory=/data/huang/tmp -nr $all_event_sorted -o $all_event_sorted
#rm -f $all_event_file
echo "event-count file (sorted by counts) extracted at $all_event_sorted"

### delete low level files.
#rm -rf $result_dir $merge_dir
