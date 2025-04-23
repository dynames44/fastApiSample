from fastapi import APIRouter, Query
from typing import Annotated, Optional
from .sample_usecase import usecase
from core.dbUtil import get_db_conn, execute_query_wo_conn, execute_query_wt_conn, execute_transaction, set_exec_result
router = APIRouter(prefix="/dbSample1"  ,include_in_schema=False ,tags=["DB Exam"])

@router.get("/singleQuery")
async def single_query():

    rtnData = await usecase.single_query()
    return rtnData

@router.get("/conditionQuery")
async def condition_query(blog_id: Annotated[int, Query(...)]):

    query : str = """
            SELECT 
                     id
                    ,title 
            FROM blog
            WHERE id >= :blog_id
            """
            
    params = {
        "blog_id": blog_id
    }            
            
    rtnData = execute_query_wt_conn(query,params)
    return rtnData

@router.get("/fineOne")
async def fineOne(blog_id: Annotated[int, Query(...)]):

    query : str = """
            SELECT 
                     id
                    ,title 
            FROM blog
            WHERE id = :blog_id
            """
            
    params = {
        "blog_id": blog_id
    }            
            
    rtnData = execute_query_wt_conn(query,params,True)
    return rtnData

@router.get("/dualQuery")
async def dual_query():
    
    rtnResult: dict = {}
    conn = get_db_conn()
    
    if conn:

        query = "SELECT id, title FROM blog"
        row = execute_query_wo_conn(conn, query)
        row1 = execute_query_wo_conn(conn, query)
        
        if row.get("result_code") == "Success" and  row1.get("result_code") == "Success" :
            rtnResult = set_exec_result("Success", "",0)
            subData = {'row': row.get("result_data"), 'row1': row1.get("result_data")}
            rtnResult["result_data"] = subData
            
        else:    
            rtnResult = ("Error" ,"조회된 건이 없습니다." ,0 ,"")
            
        return rtnResult
    
@router.get("/tranQuery")
async def transaction_query():

    query = "INSERT INTO blog (title) VALUES ('제목12')"
    query2 = "INSERT INTO system (name) VALUES ('시스템1')"
    query3 = "SELECT id, title FROM blog"

    queries = [query, query2, query3]
    #queries = [query, query3]
    rtnData = execute_transaction(queries)
    return rtnData