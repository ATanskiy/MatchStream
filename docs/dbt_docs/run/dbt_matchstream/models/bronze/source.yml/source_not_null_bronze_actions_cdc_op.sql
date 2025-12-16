
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select op
from bronze.actions_cdc
where op is null



  
  
      
    ) dbt_internal_test