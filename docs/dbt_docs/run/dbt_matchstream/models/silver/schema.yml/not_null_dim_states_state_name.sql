
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select state_name
from silver.dim_states
where state_name is null



  
  
      
    ) dbt_internal_test