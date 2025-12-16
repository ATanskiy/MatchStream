
    
    

select
    state_id as unique_field,
    count(*) as n_records

from silver.dim_states
where state_id is not null
group by state_id
having count(*) > 1


