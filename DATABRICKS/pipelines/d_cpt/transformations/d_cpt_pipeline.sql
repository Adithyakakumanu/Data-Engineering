create live table bronze_d_cpt as 
select * from workspace.silver.d_cpt_clean;

create live table silver_d_cpt as 
select row_id,category,sectionheader,subsectionheader,codesuffix,mincodeinsubsection,maxcodeinsubsection from bronze_d_cpt;

create live table gold_d_cpt as 
select * from silver_d_cpt;
