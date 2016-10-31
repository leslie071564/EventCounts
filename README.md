## Prerequisite:
#### CDB_Writer module
#### CDB_Reader module
```
    git clone git@github.com:leslie071564/CDB_handler.git
```
    
## Extract original sentences given event strings:
#### ex: (print 5 random sentences containing event "切手/きって-ヲ-貼る/はる")
```
        python event_to_sentence.py -e 切手/きって-ヲ-貼る/はる -n 5
```
#### ex: (print all sentences containing event "切手/きって-ヲ-貼る/はる")
```
        python event_to_sentence.py -e 切手/きって-ヲ-貼る/はる
```

## Build Event-count databases:
    (gxpc) ./BuildEventDatabase.sh
    will output:
        1. event-sid cdbs: /windroot/$USER/EventCounts_$DATE/Event-sid/
            (CDB_Reader module required.)
        2. event-count cdbs: /windroot/$USER/EventCounts_$DATE/Event-count/
            (CDB_Reader module required.)
        3. sorted event-count txt file: /windroot/$USER/EventCounts_$DATE/all_events_counts_sorted.txt
