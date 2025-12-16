
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select action_at
from gold.actions
where action_at is null



  
  
      
    ) dbt_internal_test