from fastapi import APIRouter
from core.dbUtil import get_db_conn, execute_query, execute_single_query

router = APIRouter(prefix="/dbSample1"  ,include_in_schema=False ,tags=["DB Exam"])
    
@router.get("/singleQuery")
async def single_query():

    query = "SELECT id, title FROM blog"
    row = execute_single_query(query)
    
    print("row::::"+row)
    return {"status": "singleQuery"}

@router.get("/dualQuery")
async def dual_query():

    conn = get_db_conn()
    if conn:

        query = "SELECT id, title FROM blog"
        row = execute_query(conn, query)
        row1 = execute_query(conn, query)
        
        print("row::::"+row)
        print("row1::::"+row1)
        return {"status": "singleQuery"}