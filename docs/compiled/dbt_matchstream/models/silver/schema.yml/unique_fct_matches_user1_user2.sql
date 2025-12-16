
    
    

select
    user1 || '-' || user2 as unique_field,
    count(*) as n_records

from silver.fct_matches
where user1 || '-' || user2 is not null
group by user1 || '-' || user2
having count(*) > 1


