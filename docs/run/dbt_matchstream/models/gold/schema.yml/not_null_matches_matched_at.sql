
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select matched_at
from gold.matches
where matched_at is null



  
  
      
    ) dbt_internal_test