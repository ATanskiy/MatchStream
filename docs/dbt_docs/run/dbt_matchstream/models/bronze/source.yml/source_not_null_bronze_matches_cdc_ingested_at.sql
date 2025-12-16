
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ingested_at
from bronze.matches_cdc
where ingested_at is null



  
  
      
    ) dbt_internal_test