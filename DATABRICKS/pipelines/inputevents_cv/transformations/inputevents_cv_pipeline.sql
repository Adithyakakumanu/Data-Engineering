create live table workspace.hospital_pipeline.bronze_inputevents_cv
as select * from workspace.gold.inputevents_cv_summary;
create live table workspace.hospital_pipeline.silver_inputevents_cv
as select hadm_id,icustay_id,amount,amountuom,rate,rateuom,stopped,originalamount,originalamountuom,originalrate,originalroute,duration from workspace.hospital_pipeline.bronze_inputevents_cv;
create live table workspace.hospital_pipeline.gold_inputevents_cv
as select icustay_id,amount,amountuom,rate,rateuom,stopped,originalamount,originalamountuom,originalrate,originalroute,duration from workspace.hospital_pipeline.silver_inputevents_cv where rate is not null;