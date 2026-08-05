create live table workspace.hospital_pipeline.bronze_labevents as
select * from workspace.gold.labevents_summary;
create live table workspace.hospital_pipeline.silver_labevents as
select hadm_id, itemid, charttime, valuenum,value,valueuom,flag from workspace.hospital_pipeline.bronze_labevents;
create live table workspace.hospital_pipeline.gold_labenevents as
select distinct itemid as itemid,charttime,valuenum,value,valueuom,flag from workspace.hospital_pipeline.silver_labevents;
