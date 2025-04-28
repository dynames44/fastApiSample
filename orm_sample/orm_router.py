from fastapi import APIRouter, Query,Depends, Body
from typing import Annotated, Optional
from .orm_model import serch_model, find_user, sys_user, user_etc
from .orm_usecase import orm_usecase as usecase

router = APIRouter(prefix="/orm"  ,tags=["DB ORM Exam"])

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

#사용자 정보 + 기타 정보 : Join  
@router.get("/get_user_join")
async def get_user_join(
    user_id: Annotated[Optional[str], Query()] = None,
    userParam: serch_model = Depends()):
    
    params_dict = userParam.model_dump()
    params_dict["user_id"] = user_id
    rtnData = await usecase.get_user_join(params_dict)
    return rtnData