create live table workspace.hospital_pipeline.bronze_inputevents_mv
as select * from workspace.gold.inputevents_mv_summary;
create live table workspace.hospital_pipeline.silver_inputevents_mv
as select hadm_id,icustay_id,amount,amountuom,rate,rateuom,ordercategoryname,secondaryordercategoryname,ordercomponenttypedescription,ordercategorydescription,patientweight,totalamount,statusdescription,originalamount,originalrate,duration from workspace.hospital_pipeline.bronze_inputevents_mv;
CREATE LIVE TABLE workspace.hospital_pipeline.gold_inputevents_mv AS
SELECT
hadm_id,
amount,
amountuom,
rate,
rateuom,
ordercategoryname,
secondaryordercategoryname,
ordercomponenttypedescription,
ordercategorydescription,
patientweight,
totalamount,
statusdescription,
originalamount,
originalrate,
duration,
COUNT(icustay_id) AS icustay_count
FROM workspace.hospital_pipeline.silver_inputevents_mv
GROUP BY
hadm_id,
amount,
amountuom,
rate,
rateuom,
ordercategoryname,
secondaryordercategoryname,
ordercomponenttypedescription,
ordercategorydescription,
patientweight,
totalamount,
statusdescription,
originalamount,
originalrate,
duration;
