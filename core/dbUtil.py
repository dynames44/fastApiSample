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

    engine = get_db_conn()
    if not engine:
        return {"status": "DB Conn 생성 실패"}
    
    try:
        
        with engine.connect() as conn:
            stmt = text(sql)
            result = conn.execute(stmt)
            rows = result.fetchall()
            return rows
            
    except SQLAlchemyError as e:
        print("쿼리 실행 오류:", e)
        return []

def execute_transaction(queries: list[str]):

    engine = get_db_conn()
    if not engine:
        return {"status": "DB Conn 생성 실패"}
    
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                for sql in queries:
                    conn.execute(text(sql))
                trans.commit()
                return {"status": "commit 완료"}
            
            except:
                trans.rollback()
                raise
            
    except SQLAlchemyError as e:
        print("트랜잭션 오류:", e)
        return {"status": "rollback됨"}

def execute_transaction_dict(queries: list[tuple[str, dict]]):
    
    engine = get_db_conn()
    if not engine:
        return {"status": "DB Conn 생성 실패"}

    try:
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                for sql, params in queries:
                    conn.execute(text(sql), params)
                trans.commit()
                return {"status": "commit 완료"}
            
            except:
                trans.rollback()
                raise
            
    except SQLAlchemyError as e:
        print("트랜잭션 오류:", e)
        return {"status": "rollback됨"}
