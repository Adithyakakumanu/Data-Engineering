create live table chartevents_bronze as select * from workspace.silver.chartevents_clean;
create live table chartevents_silver as select * from chartevents_bronze
where resultstatus!='NA' and stopped!='NA';
create live table chartevents_gold as select icustay_id,itemid,resultstatus,stopped,value,valuenum,valueuom,duration from chartevents_silver;