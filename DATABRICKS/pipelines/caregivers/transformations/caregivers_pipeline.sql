create or refresh live table bronze_caregivers as 
select * from 
workspace.silver.caregivers_clean;
create live table  silver_caregivers as 
select * from bronze_caregivers;
create  live table  gold_caregivers as 
select * from silver_caregivers;