create table  bronze_caregivers as 
select * from 
workspace.silver.caregivers_clean;

create table  silver_caregivers as
select * from 
bronze_caregivers;

create table gold_caregivers as 
select cgid,label,description from 
silver_caregivers;