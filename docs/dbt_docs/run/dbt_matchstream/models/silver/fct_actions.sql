
    -- back compat for old kwarg name
  
  
  
      
          
              
              
          
              
              
          
      
  

  

  merge into silver.fct_actions as DBT_INTERNAL_DEST
      using fct_actions__dbt_tmp as DBT_INTERNAL_SOURCE
      on 
                  DBT_INTERNAL_SOURCE.user_id = DBT_INTERNAL_DEST.user_id
               and 
                  DBT_INTERNAL_SOURCE.target_id = DBT_INTERNAL_DEST.target_id
              

      when matched then update set
         * 

      when not matched then insert *
