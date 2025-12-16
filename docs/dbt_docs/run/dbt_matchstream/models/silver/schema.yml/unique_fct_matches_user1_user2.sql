
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    user1 || '-' || user2 as unique_field,
    count(*) as n_records

from silver.fct_matches
where user1 || '-' || user2 is not null
group by user1 || '-' || user2
having count(*) > 1



  
  
      
    ) dbt_internal_test