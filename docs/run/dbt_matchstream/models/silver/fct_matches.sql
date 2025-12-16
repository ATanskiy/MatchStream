
    -- back compat for old kwarg name
  
  
  
      
          
              
              
          
              
              
          
      
  

  

  merge into silver.fct_matches as DBT_INTERNAL_DEST
      using fct_matches__dbt_tmp as DBT_INTERNAL_SOURCE
      on 
                  DBT_INTERNAL_SOURCE.user1 = DBT_INTERNAL_DEST.user1
               and 
                  DBT_INTERNAL_SOURCE.user2 = DBT_INTERNAL_DEST.user2
              

      when matched then update set
         * 

      when not matched then insert *
