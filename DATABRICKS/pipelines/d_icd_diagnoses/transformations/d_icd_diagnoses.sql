create live table bronze_d_icd_diagnoses as 
select * from workspace.silver.d_icd_diagnoses_clean;
create live table silver_d_icd_diagnoses as 
select icd9_code,short_title,long_title from bronze_d_icd_diagnoses;
create live table gold_d_icd_diagnoses as 
select count(icd9_code) as total_diagnoses,* from silver_d_icd_diagnoses
group by short_title,icd9_code,long_title;