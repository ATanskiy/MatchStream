
    
    

select
    user_id || '-' || target_id as unique_field,
    count(*) as n_records

from silver.fct_actions
where user_id || '-' || target_id is not null
group by user_id || '-' || target_id
having count(*) > 1


