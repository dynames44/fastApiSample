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
        #"dbms": decryt(os.getenv("DB_DBMS")),
        "dbms": "py_db",        
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

#DB 처리 트랜젝션구분, 커넥션 외부 주입, 일반  분기하여 처리 
def execute_query (sql: str, params: dict = None, find_one: bool = False, db_transact: bool = False, db_conn= None):
    
    rtnData = {}
    
    if db_transact and db_conn is not None: #DB 트랜젝션 처리
        rtnData = execute_query_transaction(db_conn ,sql ,params ,find_one)
    
    elif not db_transact and db_conn is not None: #DB Conn 외부 주입 - n개의 DB 처리 
        rtnData = execute_query_wo_conn(db_conn ,sql ,params ,find_one)
    
    else:
        rtnData = execute_query_wt_conn(sql ,params ,find_one)
    
    return rtnData

#DB 일반 
def execute_query_wt_conn(sql: str, params: dict = None, find_one: bool = False):
    rtnResult: dict = {}
    engine = get_db_conn()
    
    if not engine:
        return set_exec_result("Error", "DB Conn 생성 실패", 0)

    try:
        with engine.connect() as conn:
            stmt = text(sql)

            if stmt.supports_execution:  # 트랜잭션 처리 필요 시
                with conn.begin():
                    result = conn.execute(stmt, params or {})
            else:
                result = conn.execute(stmt, params or {})

            if result.returns_rows:  # SELECT 쿼리
                if find_one:
                    data = result.fetchone()
                    if data is None:
                        rtnResult = set_exec_result("Error", "조회된 건이 없습니다.", 0, "")
                    else:
                        rtnResult = set_exec_result("Success", "", 0, {k.lower(): v for k, v in data._mapping.items()})
                else:
                    dataList = result.fetchall()
                    if not dataList:
                        rtnResult = set_exec_result("Error", "조회된 건이 없습니다.", 0, "")
                    else:
                        rtnResult = set_exec_result(
                            "Success", "", len(dataList),
                            [{k.lower(): v for k, v in row._mapping.items()} for row in dataList]
                        )
            else:  # DML
                rtnResult = set_exec_result("Success", "", result.rowcount)

    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error", f"쿼리 실행 오류: {e}", 0)

    return rtnResult

#DB Conn 외부 주입 - n개의 DB 처리 
def execute_query_wo_conn(engine, sql: str, params: dict = None, find_one: bool = False):
    rtnResult: dict = {}
    
    try:
        with engine.connect() as conn:
            stmt = text(sql)

            if stmt.supports_execution:  # 트랜잭션 처리 필요 시
                with conn.begin():
                    result = conn.execute(stmt, params or {})
            else:
                result = conn.execute(stmt, params or {})

            if result.returns_rows:  # SELECT 쿼리
                if find_one:  # 단건 조회
                    data = result.fetchone()
                    
                    if data is None:
                        rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                        
                    else:
                        rtnResult = set_exec_result("Success" ,"" ,0 ,dict((k.lower(), v) for k, v in data._mapping.items()))
                        
                        
                else:  # 다건 조회
                    dataList = result.fetchall()
                    
                    if not dataList:
                        rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                    else:
                        rtnResult = set_exec_result("Success" ,"" ,len(dataList) ,[dict((k.lower(), v) for k, v in row._mapping.items()) for row in dataList])
                        
            else:  # DML 쿼리 (INSERT, UPDATE, DELETE)
                rtnResult = set_exec_result("Success" ,"" ,result.rowcount)
            
    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error" ,f"쿼리 실행 오류: {e}" ,0)
    
    return rtnResult

#DB 트랜젝션 처리
def execute_query_transaction (conn, sql: str, params: dict = None, find_one: bool = False):
    rtnResult: dict = {}

    try:
        stmt = text(sql)
        result = conn.execute(stmt, params or {})

        if result.returns_rows:
            if find_one:
                data = result.fetchone()
                if data is None:
                    rtnResult = set_exec_result("Error", "조회된 건이 없습니다.", 0, "")
                else:
                    rtnResult = set_exec_result("Success", "", 0, {k.lower(): v for k, v in data._mapping.items()})
            else:
                dataList = result.fetchall()
                if not dataList:
                    rtnResult = set_exec_result("Error", "조회된 건이 없습니다.", 0, "")
                else:
                    rtnResult = set_exec_result(
                        "Success", "", len(dataList),
                        [{k.lower(): v for k, v in row._mapping.items()} for row in dataList]
                    )
        else:
            rtnResult = set_exec_result("Success", "", result.rowcount)

    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error", f"쿼리 실행 오류: {e}", 0)

    return rtnResult