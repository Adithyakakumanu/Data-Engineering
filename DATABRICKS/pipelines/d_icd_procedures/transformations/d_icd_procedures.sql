create live table bronze_d_icd_procedures as 
select * from workspace.silver.d_icd_procedures_clean;
create live table silver_d_icd_procedures as 
select icd9_code,short_title,long_title from bronze_d_icd_procedures;
create live table gold_d_icd_procedures as 
select count(icd9_code) as total_procedures,* from silver_d_icd_procedures
group by icd9_code,short_title,long_title
order by desc;