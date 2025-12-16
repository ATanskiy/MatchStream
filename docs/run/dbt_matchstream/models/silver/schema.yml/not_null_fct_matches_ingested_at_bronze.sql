
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ingested_at_bronze
from silver.fct_matches
where ingested_at_bronze is null



  
  
      
    ) dbt_internal_test