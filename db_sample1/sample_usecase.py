from core.dbUtil import get_db_conn, set_exec_result
from sqlalchemy.exc import SQLAlchemyError
from .sample_repository import sample_repository as repository

#사용자 목록 조회 
async def get_user_list(param : dict = None):
    return await repository.get_user_list(param)

#사용자 상세정보 
async def get_user_info(param : dict):
    return await repository.get_user_info(param)

#사용자정보 + 기타 정보 : 별도 쿼리 실행 
async def get_user_all(
             userParam : dict = None
            ,etcParam : dict = None ):
    
    rtnResult: dict = {}
    
    try:
        conn = get_db_conn()
        
        if conn:
            user_list =  await repository.get_user_list(userParam ,conn=conn) 
            etcinfo_list = await repository.get_etcinfo_list(etcParam ,conn=conn)
            
            if user_list.get("result_code") == "Success" and  etcinfo_list.get("result_code") == "Success" :
                rtnResult = set_exec_result("Success", "",0)
                subData = {'user_list': user_list.get("result_data"), 'etcinfo_list': etcinfo_list.get("result_data")}
                rtnResult["result_data"] = subData
                
            else:    
                rtnResult = ("Error" ,"조회된 건이 없습니다." ,0 ,"")            

    except SQLAlchemyError:
        rtnResult = set_exec_result("Error" ,"DB Conn 생성 실패" ,0)

    except Exception as e:
        rtnResult = set_exec_result("Error" ,f"기타 오류: {e}" ,0)     

    return rtnResult

#사용자 정보 + 기타 정보 : Join  
async def get_user_join(param : dict = None):
    return await repository.get_user_join(param)

#사용자 정보 INSERT
async def insert_sys_user(param):
    return await repository.insert_sys_user(param)

#사용자 정보 UPDATE
async def update_sys_user(param):
    return await repository.update_sys_user(param)

#사용자 기타정보 INSERT
async def insert_user_etc(param):
    return await repository.insert_user_etc(param)

#사용자 기타정보 UPDATE
async def update_user_etc(param):
    return await repository.update_user_etc(param)

#사용자정보 +  기타정보 INSERT 트랜젝션 적용 
async def insert_user_dual (userParam: dict, etcParam: dict):
    
    rtnResult = {}
    engine = get_db_conn()
    
    if not engine:
        return set_exec_result("Error", "DB Conn 생성 실패", 0)

    try:
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                result1 = await repository.insert_sys_user(userParam ,True ,conn=conn)
                result2 = await repository.insert_user_etc(etcParam ,True ,conn=conn)

                #두 쿼리 모두 성공해야 커밋
                if result1["result_code"] == "Success" and result2["result_code"] == "Success":
                    trans.commit()
                    rtnResult = set_exec_result("Success", "", 2)
                else:
                    trans.rollback()
                    rtnResult = set_exec_result("Error", "트랜잭션 중 일부 실패", 0)

            except Exception as e:
                trans.rollback()
                rtnResult = set_exec_result("Error", f"트랜잭션 처리 중 오류: {e}", 0)

    except SQLAlchemyError as e:
        rtnResult = set_exec_result("Error", f"DB 오류: {e}", 0)

    return rtnResult

class usecase:
    get_user_list = staticmethod(get_user_list)
    get_user_info = staticmethod(get_user_info)
    get_user_all = staticmethod(get_user_all)
    get_user_join = staticmethod(get_user_join) 
    insert_sys_user = staticmethod(insert_sys_user)
    update_sys_user = staticmethod(update_sys_user)
    insert_user_etc = staticmethod(insert_user_etc)
    update_user_etc = staticmethod(update_user_etc)
    insert_user_dual = staticmethod(insert_user_dual)