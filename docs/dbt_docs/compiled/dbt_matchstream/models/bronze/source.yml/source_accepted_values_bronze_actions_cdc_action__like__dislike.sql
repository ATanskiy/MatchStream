
    
    

with all_values as (

    select
        action as value_field,
        count(*) as n_records

    from bronze.actions_cdc
    group by action

)

select *
from all_values
where value_field not in (
    'like','dislike'
)


