#from typing import Annotated
from .pydanticModel import ItemExtd
from pydantic import ValidationError 
from fastapi.exceptions import RequestValidationError
from fastapi import APIRouter ,Depends

router = APIRouter(prefix="/pydantic2"  ,tags=["Pydantic Model Validator Exam"])
#router = APIRouter(prefix="/pydantic2"  ,include_in_schema=False)

#Field를 이용한 Model로 받아 낸다
@router.put("/formReq/{item_id}")
async def formReq(
          item_id: int
         ,item: ItemExtd #Model Request Body로 받는다.
    ):
    rtnData = {
         "item_id": item_id
         ,"item" : item
    }
    return rtnData

@router.put("/formReq1/{item_id}")
async def formReq1(
          item_id: int
         ,item: ItemExtd #Model Request Body로 받는다.
    ):
    
    try :
        rtnData = {
            "item_id": item_id
            ,"item" : item
        }
        return rtnData
    
    except ValidationError as e:
        raise RequestValidationError(e.errors())
    
@router.put("/formReq2")
async def formReq2(
         item: ItemExtd #Model Request Body로 받는다.
    ):
    
    try :
        rtnData = item
        return rtnData
    
    except ValidationError as e:
        raise RequestValidationError(e.errors())    
    
@router.get("/getReq")
async def getReq(
         item: ItemExtd = Depends()  #Depends 사용 GET으로 받아도 Model을 사용할 수 있다.
    ):
    
    try :
        rtnData = item
        return rtnData
    
    except ValidationError as e:
        raise RequestValidationError(e.errors())