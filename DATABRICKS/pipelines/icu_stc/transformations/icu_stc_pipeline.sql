create live table workspace.hospital_pipeline.bronze_data1
as select * from workspace.gold.icustays_summary;
create live table workspace.hospital_pipeline.bronze_data2
as select * from workspace.gold.services_summary;
create live table workspace.hospital_pipeline.bronze_data3
as select * from workspace.gold.transfers_summary;
create live table workspace.hospital_pipeline.silver_data1
as select b2.* ,b1.icustay_id,b1.dbsource,b1.first_careunit,b1.last_careunit,b1.first_wardid,b1.last_wardid,b1.los as service_duration from workspace.hospital_pipeline.bronze_data1 as b1 join workspace.hospital_pipeline.bronze_data2 as b2 on b1.subject_id=b2.subject_id;
create live table workspace.hospital_pipeline.silver_data2
as select b2.transfertime,b2.prev_service,b2.curr_service,b3.* from workspace.hospital_pipeline.bronze_data2 as b2 join workspace.hospital_pipeline.bronze_data3 as b3 on b2.subject_id=b3.subject_id;
create live table workspace.hospital_pipeline.gold_data
as select s1.subject_id,s1.hadm_id,s1.icustay_id,s1.dbsource,s1.first_careunit,s1.last_careunit,s1.first_wardid,s1.last_wardid,s1.service_duration,s2.eventtype,s2.transfertime,s2.prev_service,s2.curr_service,s2.prev_careunit,s2.curr_careunit,s2.prev_wardid,s2.curr_wardid,s2.los as transfers_duration from workspace.hospital_pipeline.silver_data1 as s1 join workspace.hospital_pipeline.silver_data2 as s2 on s1.subject_id=s2.subject_id;