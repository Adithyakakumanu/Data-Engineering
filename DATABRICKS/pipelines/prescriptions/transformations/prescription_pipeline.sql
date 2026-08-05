
create live table workspace.hospital_pipeline.bronze_prescription 
select * from workspace.gold.prescriptions_summary;
create live table workspace.hospital_pipeline.silver_prescription 
select hadm_id,icustay_id,drug,drug_type,drug_name_poe,drug_name_generic,formulary_drug_cd,ndc,dose_val_rx,dose_unit_rx,prod_strength,route,form_val_disp,form_unit_disp,duration from workspace.hospital_pipeline.bronze_prescription;
CREATE LIVE TABLE workspace.hospital_pipeline.gold_prescription AS
SELECT
COUNT(icustay_id) AS total_persons,
drug,
drug_type,
drug_name_poe,
drug_name_generic,
formulary_drug_cd,
prod_strength,
route,
duration
FROM workspace.hospital_pipeline.silver_prescription
GROUP BY
drug,
drug_type,
drug_name_poe,
drug_name_generic,
formulary_drug_cd,
prod_strength,
route,
duration;