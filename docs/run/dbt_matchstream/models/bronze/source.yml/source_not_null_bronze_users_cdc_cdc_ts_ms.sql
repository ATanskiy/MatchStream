
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select cdc_ts_ms
from bronze.users_cdc
where cdc_ts_ms is null



  
  
      
    ) dbt_internal_test