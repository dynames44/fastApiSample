import os
from core.cryto import decryt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def load_conn_env():
    load_dotenv()
    return {
        "host": decryt(os.getenv("DB_HOST")),
        "port": decryt(os.getenv("DB_PORT")),
        "user": decryt(os.getenv("DB_USER")),
        "passwd": decryt(os.getenv("DB_PASSWD")),
        "dbms": "py_db",        
    }
    
def get_connection_url(envs):
    return f"mariadb+mariadbconnector://{envs['user']}:{envs['passwd']}@{envs['host']}:{envs['port']}/{envs['dbms']}"    
    
def get_db_session ():
    
    envs = load_conn_env()
    conn_str = get_connection_url(envs)
    
    # 엔진 및 세션 팩토리 생성
    engine = create_engine(conn_str, echo=True, future=True)
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    
    return session_factory
    
    
def get_db_commit_session ():
    
    envs = load_conn_env()
    conn_str = get_connection_url(envs)
    
    # 엔진 및 세션 팩토리 생성
    engine = create_engine(conn_str, echo=True, future=True)
    session_factory = sessionmaker(bind=engine, autocommit=True, autoflush=True)
    
    return session_factory
    
    
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