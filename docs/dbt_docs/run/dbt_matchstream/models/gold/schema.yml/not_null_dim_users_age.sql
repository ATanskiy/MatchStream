
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select age
from gold.dim_users
where age is null



  
  
      
    ) dbt_internal_test