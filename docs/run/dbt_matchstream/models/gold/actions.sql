
  
    
        create or replace table gold.actions
      
      
    using iceberg
      
      
      
      
      
      

      as
      

SELECT
    user_id,
    target_id,
    action,
    created_at AS action_at,
    DATE(created_at) AS action_date

FROM silver.fct_actions
  