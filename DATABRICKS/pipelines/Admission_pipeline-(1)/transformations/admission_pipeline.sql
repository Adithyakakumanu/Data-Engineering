create materialized view  bronze_admission as 
select * from 
workspace.silver.admissions_clean;

create materialized view  silver_admission as
select * from 
bronze_admission;

create materialized view  gold_admission as 
select * from 
silver_admission;