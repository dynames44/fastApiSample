import os
import urllib.parse
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text

#key = Fernet.generate_key() #매번 실행때 마다 새키를 발급 하면 에러....
key = b'aW8wmBIBdB61OF3duw-qZwtH_Qp7UIifgkYydgCBs_8=' #키값은 고정 
cipher = Fernet(key)

def encryt(param : str):
    enc_encode = urllib.parse.quote(param)
    enc_pass = cipher.encrypt(enc_encode.encode())
    return enc_pass

def decryt(param : str):
    dec_pass = cipher.decrypt(param.encode()).decode()
    return dec_pass

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

def execute_query(engine, sql: str):
    try:
        with engine.connect() as conn:
            stmt = text(sql)
            result = conn.execute(stmt)
            rows = result.fetchall()
            return rows
    except SQLAlchemyError as e:
        print("쿼리 실행 오류:", e)
        return []

def execute_single_query(sql: str):
    try:
        
        engine = get_db_conn()
        
        if engine:
            with engine.connect() as conn:
                stmt = text(sql)
                result = conn.execute(stmt)
                rows = result.fetchall()
                return rows
            
    except SQLAlchemyError as e:
        print("쿼리 실행 오류:", e)
        return []
    
def test1():
    engine = get_db_conn()
    if engine:
        rows = execute_query(engine, "SELECT id, title FROM blog")
        rows1 = execute_query(engine, "SELECT id, title FROM blog")
        print("rows::::::",rows)    
        print("rows1::::::",rows1)    
        
def test2():
    rows = execute_single_query("SELECT id, title FROM blog")
    print("rows::::::",rows)    

test1()
print(":::::::::::::")
test2()