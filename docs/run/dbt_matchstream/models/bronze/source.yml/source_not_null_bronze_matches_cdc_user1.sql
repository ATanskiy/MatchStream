
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select user1
from bronze.matches_cdc
where user1 is null



  
  
      
    ) dbt_internal_test