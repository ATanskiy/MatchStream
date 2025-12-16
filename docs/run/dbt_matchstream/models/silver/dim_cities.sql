
    -- back compat for old kwarg name
  
  
  
      
          
          
      
  

  

  merge into silver.dim_cities as DBT_INTERNAL_DEST
      using dim_cities__dbt_tmp as DBT_INTERNAL_SOURCE
      on 
              DBT_INTERNAL_SOURCE.city_id = DBT_INTERNAL_DEST.city_id
          

      when matched then update set
         * 

      when not matched then insert *
