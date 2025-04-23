from core.dbUtil import get_db_conn, execute_query_wo_conn, execute_query_wt_conn, execute_transaction, set_exec_result

async def single_query(params : dict = None):

    query : str = """
            SELECT 
                     id
                    ,title 
            FROM blog
            """
    rtnData = execute_query_wt_conn(query,params)
    return rtnData

class sample_repository:
    single_query = staticmethod(single_query)


#sample_repository