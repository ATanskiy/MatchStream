
    -- back compat for old kwarg name
  
  
  
      
          
          
      
  

  

  merge into silver.dim_states as DBT_INTERNAL_DEST
      using dim_states__dbt_tmp as DBT_INTERNAL_SOURCE
      on 
              DBT_INTERNAL_SOURCE.state_id = DBT_INTERNAL_DEST.state_id
          

      when matched then update set
         * 

      when not matched then insert *
