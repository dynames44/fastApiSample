import os
from core.cryto import decryt
#from .cryto import decryt
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text

def load_conn_env():
    load_dotenv()
    return {
        "host": decryt(os.getenv("DB_HOST")),
        "port": decryt(os.getenv("DB_PORT")),
        "user": decryt(os.getenv("DB_USER")),
        "passwd": decryt(os.getenv("DB_PASSWD")),
        "dbms": decryt(os.getenv("DB_DBMS")),
    }

def get_connection_url(envs):
    return f"mariadb+mariadbconnector://{envs['user']}:{envs['passwd']}@{envs['host']}:{envs['port']}/{envs['dbms']}"
    #DATABASE_CONN = "mariadb+mariadbconnector://root:qwe123%23%40%21@localhost:9306/blog_db"    

def get_db_conn():
    engine = None
    try:
        envs = load_conn_env()
        conn_url = get_connection_url(envs)
        engine = create_engine(
            conn_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=0
        )
    except SQLAlchemyError as e:
        print("DB 오류:", e)
        
    return engine

def set_exec_result(result_code : str, result_msg : str , result_count : int,  result_data = None):
    
    rtnResult: dict = {}
    rtnResult["result_code"] = result_code
    
    if result_msg is None or result_msg == "" :
        rtnResult["result_msg"] = "정상처리 되었습니다."
        
    else:
        rtnResult["result_msg"] = result_msg
        
    rtnResult["result_count"] = result_count
    rtnResult["result_data"] = result_data
    return rtnResult 

def execute_query_wt_conn(sql: str, params: dict = None, find_one: bool = False):
    rtnResult: dict = {}
    engine = get_db_conn()
    
    if not engine:
        rtnResult = set_exec_result("Error" ,"DB Conn 생성 실패" ,0)
        return rtnResult
    
    try:
        with engine.connect() as conn:
            stmt = text(sql)
            result = conn.execute(stmt, params or {})
            
            if result.returns_rows:  # SELECT 쿼리
                if find_one:  # 단건 조회
                    data = result.fetchone()
                    
                    if data is None:
                       rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")     
                    else:
                       rtnResult = set_exec_result("Success" ,"" ,0 ,dict(data._mapping))
                        
                else:  # 다건 조회
                    dataList = result.fetchall()
                    
                    if not dataList:
                       rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                    else:
                        rtnResult = set_exec_result("Success" ,"" ,len(dataList) ,[dict(data._mapping) for data in dataList])
                        
            else:  # DML 쿼리 (INSERT, UPDATE, DELETE)
                rtnResult = set_exec_result("Success" ,"" ,result.rowcount)
            
    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error" ,f"쿼리 실행 오류: {e}" ,0)
    
    return rtnResult


def execute_query_wo_conn(engine, sql: str, params: dict = None, find_one: bool = False):
    rtnResult: dict = {}
    
    try:
        with engine.connect() as conn:
            stmt = text(sql)
            result = conn.execute(stmt, params or {})
            
            if result.returns_rows:  # SELECT 쿼리
                if find_one:  # 단건 조회
                    data = result.fetchone()
                    
                    if data is None:
                        rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                        
                    else:
                        rtnResult = set_exec_result("Success" ,"" ,0 ,dict(data._mapping))
                        
                        
                else:  # 다건 조회
                    dataList = result.fetchall()
                    
                    if not dataList:
                        rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                    else:
                        rtnResult = set_exec_result("Success" ,"" ,len(dataList) ,[dict(data._mapping) for data in dataList])
                        
            else:  # DML 쿼리 (INSERT, UPDATE, DELETE)
                rtnResult = set_exec_result("Success" ,"" ,result.rowcount)
            
    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error" ,f"쿼리 실행 오류: {e}" ,0)
    
    return rtnResult


def execute_single_query(sql: str, find_one: bool = False):
    rtnResult: dict = {}
    engine = get_db_conn()
    
    if not engine:
        rtnResult = set_exec_result("Error" ,"DB Conn 생성 실패" ,0)
        return rtnResult
    
    try:
        with engine.connect() as conn:
            stmt = text(sql)
            result = conn.execute(stmt)
            
            if result.returns_rows:  # SELECT 쿼리
                if find_one:  # 단건 조회
                    data = result.fetchone()
                    
                    if data is None:
                       rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")     
                    else:
                       rtnResult = set_exec_result("Success" ,"" ,0 ,dict(data._mapping))
                        
                else:  # 다건 조회
                    dataList = result.fetchall()
                    
                    if not dataList:
                       rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                    else:
                        rtnResult = set_exec_result("Success" ,"" ,len(dataList) ,[dict(data._mapping) for data in dataList])
                        
            else:  # DML 쿼리 (INSERT, UPDATE, DELETE)
                rtnResult = set_exec_result("Success" ,"" ,result.rowcount)
            
    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error" ,f"쿼리 실행 오류: {e}" ,0)
    
    return rtnResult

def execute_transaction(queries: list[str]):
    
    #last_result = None
    rtnResult: dict = {}
    engine = get_db_conn()
    
    if not engine:
        rtnResult = set_exec_result("Error" ,"DB Conn 생성 실패" ,0)
        return rtnResult

    try:
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                for idx, sql in enumerate(queries):
                    conn.execute(text(sql))
                    # #마지막 실행하는 쿼리의 실행 결과를 리턴한다.
                    # if idx == len(queries) - 1:
                    #     last_result = result.fetchall()
                trans.commit()
                rtnResult = set_exec_result("Success" ,"" ,0)
            
            except:
                trans.rollback()
                raise
            
    except SQLAlchemyError as e:
        print("트랜잭션 오류:", e)
        rtnResult = set_exec_result("Error" ,f"트랜잭션 오류: {e}" ,0)
    
    return rtnResult

# def execute_transaction_dict(queries: list[tuple[str, dict]]):
    
#     engine = get_db_conn()
#     if not engine:
#         return {"status": "DB Conn 생성 실패"}

#     try:
#         with engine.connect() as conn:
#             trans = conn.begin()
            
#             try:
#                 for sql, params in queries:
#                     conn.execute(text(sql), params)
#                 trans.commit()
#                 return {"status": "commit 완료"}
            
#             except:
#                 trans.rollback()
#                 raise
            
#     except SQLAlchemyError as e:
#         print("트랜잭션 오류:", e)
#         return {"status": "rollback됨"}


# def execute_query(engine, sql: str, find_one: bool = False):
    
#     rtnResult: dict = {}
    
#     try:
#         with engine.connect() as conn:
#             stmt = text(sql)
#             result = conn.execute(stmt)
            
#             if result.returns_rows:  # SELECT 쿼리
#                 if find_one:  # 단건 조회
#                     data = result.fetchone()
                    
#                     if data is None:
#                         rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                        
#                     else:
#                         rtnResult = set_exec_result("Success" ,"" ,0 ,dict(data._mapping))
                        
                        
#                 else:  # 다건 조회
#                     dataList = result.fetchall()
                    
#                     if not dataList:
#                         rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
#                     else:
#                         rtnResult = set_exec_result("Success" ,"" ,len(dataList) ,[dict(data._mapping) for data in dataList])
                        
#             else:  # DML 쿼리 (INSERT, UPDATE, DELETE)
#                 rtnResult = set_exec_result("Success" ,"" ,result.rowcount)
            
#     except SQLAlchemyError as e:
#         rtnResult = set_exec_result("Error" ,f"쿼리 실행 오류: {e}" ,0)
    
#     return rtnResult