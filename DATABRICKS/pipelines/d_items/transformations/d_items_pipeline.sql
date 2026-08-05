create live table bronze_d_items as 
select * from workspace.silver.d_items_clean;
create live table silver_d_items as 
select itemid,label,abbreviation,dbsource,linksto,category,unitname,param_type from bronze_d_items where category!='NA';
create live table gold_d_items as 
select count(itemid) as total_items,*  as total_procedures,* from silver_d_items
group by category;