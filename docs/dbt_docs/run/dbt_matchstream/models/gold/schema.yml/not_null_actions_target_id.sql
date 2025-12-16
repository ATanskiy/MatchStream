
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select target_id
from gold.actions
where target_id is null



  
  
      
    ) dbt_internal_test