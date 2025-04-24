from core.dbUtil import get_db_conn, execute_query_wo_conn, execute_query_wt_conn, execute_transaction, set_exec_result

#사용자 목록 조회 
async def get_user_list(params : dict = None, conn = None):

    rtnData = {}
    conditions = []     
    query_base : str = """
            SELECT 
                     A.USER_ID
                    ,A.USER_NM 
                    ,A.USER_PW
                    ,A.USE_YN
                    ,A.EMAIL
                    ,A.REG_DTTM
            FROM tb_sys_user A
            """

    if params and params.get("use_yn") is not None:
       conditions.append("A.USE_YN = :use_yn")               
       
    if params and params.get("email") is not None:
       conditions.append("A.EMAIL LIKE CONCAT('%', :email, '%')")
    
    if conditions:
        query_base += " WHERE " + " AND ".join(conditions)    

    #외부에서 DB연결을 했으면 해당 커넥션을 사용 
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,params)
    else:
        rtnData = execute_query_wt_conn(query_base,params)
    
    return rtnData

#사용자 상세정보 
async def get_user_info(params : dict ,conn = None):
    
    rtnData = {}
    query_base : str = """
            SELECT 
                     A.USER_ID
                    ,A.USER_NM 
                    ,A.USER_PW
                    ,A.USE_YN
                    ,A.EMAIL
                    ,A.REG_DTTM
            FROM    tb_sys_user A
            WHERE   A.USER_ID = :user_id
            """
    
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,params,True)
    else:
        rtnData = execute_query_wt_conn(query_base,params,True)    
    
    return rtnData

#사용자 기타정보보 조회 
async def get_etcinfo_list(params : dict = None ,conn = None):

    rtnData = {}
    conditions = []     
    query_base : str = """
            SELECT 
                     A.USER_ID
                    ,A.ETC_INFO1 
                    ,A.ETC_INFO2
                    ,A.ETC_INFO3
                    ,A.ETC_INFO4
                    ,A.ETC_INFO5                    
                    ,A.REG_DTTM
            FROM tb_user_etc A
            """

    if params and params.get("user_id") is not None:
       conditions.append("A.USER_ID = :user_id")               
    
    if conditions:
        query_base += " WHERE " + " AND ".join(conditions)    
        
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,params)
    else:
        rtnData = execute_query_wt_conn(query_base,params)
    
    return rtnData

#사용자 정보 + 기타 정보 : Join  
async def get_user_join(params : dict = None ,conn = None):

    rtnData = {}
    conditions = []     
    query_base : str = """
            SELECT 
                     A.USER_ID
                    ,A.USER_NM 
                    ,A.USER_PW
                    ,A.USE_YN
                    ,A.EMAIL
                    ,B.ETC_INFO1 
                    ,B.ETC_INFO2
                    ,B.ETC_INFO3
                    ,B.ETC_INFO4
                    ,B.ETC_INFO5                                     
                    ,A.REG_DTTM
            FROM    tb_sys_user A
                    Left Outer Join tb_user_etc B
                    On A.USER_ID = B.USER_ID
            """
    if params and params.get("user_id") is not None:
       conditions.append("A.USER_ID = :user_id")                           

    if params and params.get("use_yn") is not None:
       conditions.append("A.USE_YN = :use_yn")               
       
    if params and params.get("email") is not None:
       conditions.append("A.EMAIL LIKE CONCAT('%', :email, '%')")
    
    if conditions:
        query_base += " WHERE " + " AND ".join(conditions)    
        
    #print("query_base::::",query_base)   
    #query_base += " ORDER BY A.USER_ID ASC "       
        
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,params)
    else:
        rtnData = execute_query_wt_conn(query_base,params)
        
    return rtnData

#사용자 정보 insert
async def insert_sys_user(params : dict ,conn = None):
    
    values = []
    columns = []
    rtnData = {}
    data_params = {}
    field_list = ["user_id", "user_nm", "user_pw", "use_yn", "email"]     

    for field in field_list:
       value = params.get(field)
       
       if value is not None:
           columns.append(field.upper())         # SQL용 컬럼명
           values.append(f":{field}")            # 바인딩용 플레이스홀더
           data_params[field] = value            # 바인딩 파라미터 값

    query_base = (
        "INSERT INTO tb_sys_user "
        f"({', '.join(columns)}) "
        f"VALUES ({', '.join(values)})"
    )
        
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,data_params)
    else:
        rtnData = execute_query_wt_conn(query_base,data_params)
        
    return rtnData

#사용자 정보 update
async def update_sys_user(params : dict ,conn = None):
    
    rtnData = {}
    set_columns = []
    data_params = {}
    field_list = ["user_id", "user_nm", "user_pw", "use_yn", "email"]     

    for field in field_list:
        value = params.get(field)
        if value is not None:
            set_columns.append(f"{field.upper()} = :{field}")
            data_params[field] = value
            
    data_params["user_id"] = params["user_id"]    

    query_base = (
       "UPDATE tb_sys_user SET "
        f"{', '.join(set_columns)} "
        "WHERE USER_ID = :user_id"
    )
        
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,data_params)
    else:
        rtnData = execute_query_wt_conn(query_base,data_params)
        
    return rtnData

#사용자 기타정보 insert
async def insert_user_etc(params : dict ,conn = None):
    
    values = []
    columns = []
    rtnData = {}
    data_params = {}
    field_list = ["user_id", "etc_info1", "etc_info2", "etc_info3", "etc_info4", "etc_info5"]     

    for field in field_list:
       value = params.get(field)
       
       if value is not None:
           columns.append(field.upper())         # SQL용 컬럼명
           values.append(f":{field}")            # 바인딩용 플레이스홀더
           data_params[field] = value            # 바인딩 파라미터 값

    query_base = (
        "INSERT INTO tb_user_etc "
        f"({', '.join(columns)}) "
        f"VALUES ({', '.join(values)})"
    )
        
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,data_params)
    else:
        rtnData = execute_query_wt_conn(query_base,data_params)
        
    return rtnData

#사용자 기타정보 update
async def update_user_etc(params : dict ,conn = None):
    
    rtnData = {}
    set_columns = []
    data_params = {}
    field_list = ["user_id", "etc_info1", "etc_info2", "etc_info3", "etc_info4", "etc_info5"]

    for field in field_list:
        value = params.get(field)
        if value is not None:
            set_columns.append(f"{field.upper()} = :{field}")
            data_params[field] = value
            
    data_params["user_id"] = params["user_id"]    

    query_base = (
       "UPDATE tb_user_etc SET "
        f"{', '.join(set_columns)} "
        "WHERE USER_ID = :user_id"
    )
        
    if conn is not None:    
        rtnData = execute_query_wo_conn(conn,query_base,data_params)
    else:
        rtnData = execute_query_wt_conn(query_base,data_params)
        
    return rtnData

class sample_repository:
    get_user_list = staticmethod(get_user_list)
    get_user_info = staticmethod(get_user_info)
    get_etcinfo_list = staticmethod(get_etcinfo_list)
    get_user_join = staticmethod(get_user_join)    
    insert_sys_user = staticmethod(insert_sys_user)
    update_sys_user = staticmethod(update_sys_user)
    insert_user_etc = staticmethod(insert_user_etc)
    update_user_etc = staticmethod(update_user_etc)

