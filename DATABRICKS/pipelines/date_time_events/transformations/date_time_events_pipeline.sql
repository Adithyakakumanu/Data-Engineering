create live table date_time_events_bronze as select * from workspace.silver.datetimeevents_clean;
create live table date_time_events_silver as select row_id,icustay_id,cgid,value,stopped,duration from date_time_events_bronze where stopped!='NA' ;
create live table date_time_events_gold as select * from date_time_events_silver;