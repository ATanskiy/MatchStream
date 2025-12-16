
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        op as value_field,
        count(*) as n_records

    from bronze.users_cdc
    group by op

)

select *
from all_values
where value_field not in (
    'c','u','d','r'
)



  
  
      
    ) dbt_internal_test