
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select cdc_ts_ms
from silver.fct_matches
where cdc_ts_ms is null



  
  
      
    ) dbt_internal_test