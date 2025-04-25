from fastapi import APIRouter, Query,Depends, Body
from typing import Annotated, Optional
from .sample_usecase import usecase
from .sample_model import serch_model, find_user, sys_user, user_etc

router = APIRouter(prefix="/dbSample1"  ,tags=["DB Exam"])

# #사용자 정보 조회  
@router.get("/get_user_list")
async def get_user_list(
    use_yn: Annotated[Optional[str], Query()] = None,
    email: Annotated[Optional[str], Query()] = None,
):
    params = dict(
         use_yn = use_yn
        ,email = email
    )

    rtnData = await usecase.get_user_list(params)
    return rtnData

#사용자 정보 조회 :  파라미터를 데이터 모델로 받는다.
@router.get("/get_user_list_extd")
async def get_user_list_extd(params: serch_model = Depends()):

    params_dict : dict = params.model_dump() #모델로 받은것을 딕셔너리로 변환 : 뒤에 처리 레벨의 일관성 유지 
    rtnData = await usecase.get_user_list(params_dict)
    return rtnData

#사용자 상세 조회  
@router.get("/get_user_info")
async def get_user_info(params: find_user = Depends()):

    params_dict : dict = params.model_dump()
    rtnData = await usecase.get_user_info(params_dict)
    return rtnData

#사용자정보 + 기타 정보 : 별도 쿼리 실행 
@router.get("/get_user_all")
async def get_user_all(
    user_id: Annotated[Optional[str], Query()] = None,
    userParam: serch_model = Depends()):
    
    etcParam = dict(
         user_id = user_id
    )    
    
    params_dict = userParam.model_dump()
    rtnData = await usecase.get_user_all(params_dict,etcParam)
    return rtnData

#사용자 정보 + 기타 정보 : Join  
@router.get("/get_user_join")
async def get_user_join(
    user_id: Annotated[Optional[str], Query()] = None,
    userParam: serch_model = Depends()):
    
    params_dict = userParam.model_dump()
    params_dict["user_id"] = user_id
    rtnData = await usecase.get_user_join(params_dict)
    return rtnData

#사용자 정보 INSERT
@router.post("/insert_sys_user")
async def insert_sys_user( param: sys_user):
    
    params_dict = param.model_dump()
    rtnData = await usecase.insert_sys_user(params_dict)
    return rtnData

#사용자 정보 UPDATE
@router.post("/update_sys_user")
async def update_sys_user( param: sys_user):
    
    params_dict = param.model_dump()
    rtnData = await usecase.update_sys_user(params_dict)
    return rtnData

#사용자 기타정보 INSERT
@router.post("/insert_user_etc")
async def insert_user_etc( param: user_etc):
    
    params_dict = param.model_dump()
    rtnData = await usecase.insert_user_etc(params_dict)
    return rtnData

#사용자 기타정보 UPDATE
@router.post("/update_user_etc")
async def update_user_etc( param: user_etc):
    
    params_dict = param.model_dump()
    rtnData = await usecase.update_user_etc(params_dict)
    return rtnData

#사용자정보 +  기타정보 INSERT 트랜젝션 적용 
@router.post("/insert_user_dual")
async def insert_user_dual( 
                 sys_user_param: sys_user = Body(...)
                ,user_etc_param: user_etc = Body(...)
          ):
    
    sys_user_dict = sys_user_param.model_dump()
    user_etc_dict = user_etc_param.model_dump()
    
    rtnData = await usecase.insert_user_dual(sys_user_dict, user_etc_dict)
    return rtnData

# @router.get("/tranQuery")
# async def transaction_query():

#     query = "INSERT INTO blog (title) VALUES ('제목12')"
#     query2 = "INSERT INTO system (name) VALUES ('시스템1')"
#     query3 = "SELECT id, title FROM blog"

#     queries = [query, query2, query3]
#     #queries = [query, query3]
#     rtnData = execute_transaction(queries)
#     return rtnData