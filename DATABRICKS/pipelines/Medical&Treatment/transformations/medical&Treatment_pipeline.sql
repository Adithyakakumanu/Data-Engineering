 create live table bronze_inputevents_cv as 
 select * from workspace.gold.inputevents_cv_summary;
 create live table bronze_inputevents_mv as
 select * from workspace.gold.inputevents_mv_summary;
 create live table bronze_outputevents as
 select * from workspace.gold.outputevents_summary;
 create live table bronze_prescription as 
 select * from workspace.gold.prescriptions_summary;
 create live table bronze_procedureevents_mv as 
 select * from workspace.gold.procedureevents_mv_summary;
 create live table silver_data as 
 select cv.amount,cv.amountoum,cv.rate,cv.rateuom,cv.originalrate,cv.originalroute,cv.stopped,cv.originalamount,cv.originalamountuom,op.hadm_id,op.icustay_id,op.value,op.valeuom from bronze_inputevents_cv as cv join bronze_outputevents as op on cv.icustay_id = op.icustay_id ;
 create live table silver_data2 as 
 select mv.hadm_id,mv.icustay_id,mv.amount,mv.amountoum,mv.rate,mv.rateuom,mv.ordercategoryname,mv.ordercategorydescription,mv.statusdescription,mv.secondoryordercategoryname,mv.ordercomponenttypedescription,mv.patientweight,mv.originalamount,mv.originalrate,pr.drug,pr.drug_type,pr.drug_name_generic,pr.formulary_drug_cd,pr.drug_name_poe,pr.formulary_drug_cd,pr.dose_val_rx,pr.dose_unit_rx,pr.prod_strengthpr.route,pr.form_unit_diso from bronze_inputevents_mv as mv join bronze_prescription as pr on mv.icustay_id = pr.icustay_id;
 create live table silver_data3 as 
 select pmv.hadm_id,pmv.icustay_id,pmv.location,pmv.locationcategory,pmv.ordercategoryname,pmv.ordercategorydescription,op.duration from bronze_procedureevents_mv pmv join bronze_outputevents op on pmv.hadm_id = op.hadm_id;
alter table silver_data2 rename column amount to mv_amount;
alter table silver_data2 rename column amountoum to mv_amountoum;
alter table silver_data2 rename column rate to mv_rate;
alter table silver_data2 rename column rateuom to mv_rateuom;

ALTER TABLE silver_data3 RENAME COLUMN duration TO output_duration;
alter table silver_data3 rename column ordercategoryname to procedure_ordercategoryname;
alter table silver_data3 rename column ordercategorydescription to procedure_ordercategorydescription;