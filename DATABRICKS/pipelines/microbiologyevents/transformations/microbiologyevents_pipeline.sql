create live table workspace.hospital_pipeline.bronze_microbiologyevents 
select * from workspace.gold.microbiologyevents_summary;
create live table workspace.hospital_pipeline.silver_microbiologyevents 
select hadm_id,spec_type_desc,isolate_num,dilution_value,org_name,ab_itemid,ab_name,interpretation,duration from workspace.hospital_pipeline.bronze_microbiologyevents;
CREATE LIVE TABLE workspace.hospital_pipeline.gold_microbiologyevents AS
SELECT
COUNT(hadm_id) AS total_count,
org_name,
ab_name,
spec_type_desc,
interpretation,
ab_itemid,
duration,
dilution_value
FROM workspace.hospital_pipeline.silver_microbiologyevents
where ab_itemid IS NOT NULL
GROUP BY
org_name,
ab_name,
spec_type_desc,
interpretation,
ab_itemid,
duration,
dilution_value;