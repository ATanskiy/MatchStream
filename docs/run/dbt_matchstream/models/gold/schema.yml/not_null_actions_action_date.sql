
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select action_date
from gold.actions
where action_date is null



  
  
      
    ) dbt_internal_test