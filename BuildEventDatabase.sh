#!/bin/bash
NICE="nice -n 19"
export LC_ALL=C

result_dir="$1"
mkdir -p $result_dir

# generate config files.
config_file="$result_dir/config.sh"
python write_config.py "$@" --output_fn $config_file
source $config_file

# mkdir for some tmp folders.
gxpc e mkdir -p $extract_tmp_dir $sort_tmp_dir

# extract events from files in raw_dir.
print_task_script="./print_task.py"
extract_task_fn="./extract.task"
python $print_task_script --event_extract_task --config_fn $config_file --task_fn $extract_task_fn
echo $extract_task_fn
gxpc js -a work_file=extract.task -a cpu_factor=0.25

# merge recursively
merge_task_file=./merge.task
#while:
n=0
until [ $n -ge 10 ]
do
    echo depth $n
    n=$[$n+1]

    python ./print_task.py --merge_task --config_fn $config_file --task_fn $merge_task_file
    if [ -s $merge_task_file ];
    then
        gxpc js -a work_file=merge.task -a cpu_factor=0.25
    else 
        echo "finished merging."
        break
    fi

done
# build db
build_script=./build_event_db.py
all_events_file=$result_dir/all_events.txt

if $extract_sid;
then
    mkdir -p $result_dir/event_sid
    evSID_cdb_prefix=$result_dir/event_sid/event_sid.cdb
    python $build_script --build_event_sid_db --input_file $all_events_file --cdb_prefix $evSID_cdb_prefix

    tmp=$all_events_file.tmp
    awk '!($3="")' $all_events_file > $tmp && mv $tmp $all_events_file
fi

mkdir -p $result_dir/event_count
evCount_cdb_prefix=$result_dir/event_count/event_count.cdb
python $build_script --build_event_count_db --input_file $all_events_file --cdb_prefix $evCount_cdb_prefix

# sort event_count_file 
sort --parallel=10 --temporary-directory=sort_tmp_dir -nr $all_events_file -o $all_events_file

# delete tmp dir
gxpc e rm -rf $extract_tmp_dir $sort_tmp_dir
