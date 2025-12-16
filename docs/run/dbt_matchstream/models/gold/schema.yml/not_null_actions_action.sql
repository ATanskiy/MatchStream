
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select action
from gold.actions
where action is null



  
  
      
    ) dbt_internal_test