create live table bronze_drgcodes as
select * from workspace.silver.drgcodes_clean;
create live table silver_drgcodes as
select hadm_id, drg_code, description,drg_type from bronze_drgcodes;
create live table gold_drgcodes as
select any_value(drg_code) as drg_code,any_value(drg_type) as drg_type,description,count(hadm_id) as total_persons from silver_drgcodes
group by description;
