create live table bronze_d_labitems as 
select * from workspace.silver.d_labitems_clean;
create live table silver_d_labitems as 
select itemid,label, fluid, category from bronze_d_labitems;
create live table gold_d_labitems as 
select count(itemid) as total_labitems,label,any_value(fluid) as fluid,any_value(category) as category from silver_d_labitems
group by label
order by total_labitems desc;