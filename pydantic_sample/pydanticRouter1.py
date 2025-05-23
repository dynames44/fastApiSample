from typing import Annotated, Optional
from .pydanticModel import Item
from pydantic import ValidationError 
from fastapi.exceptions import RequestValidationError
from fastapi import APIRouter, Path, Query, Form, Depends

router = APIRouter(prefix="/pydantic1" ,tags=["Pydantic Validator Exam"])
#router = APIRouter(prefix="/pydantic1"  ,include_in_schema=False)

# Path, Query, Request Body(json)
@router.put("/items/{item_id}")
async def update_item(
          item_id: int # path param
         ,test : str   # query param : Model 에 포함된 값이 아니니.... 
         ,item: Item = None #Model Request Body로 받는다.
    ):
    rtnData = {
         "item_id": item_id
         ,"test" : test
         ,"item" : item
    }
    return rtnData

# Path, Query, Request Body(json)
# query param을 명시적으로 변경 
@router.put("/items_json/{item_id}")
async def update_item_json(
        item_id: int = Path(..., gt=0), #Path Param으로 받음.. Path(..제약조건 기술)
        test1: Annotated[str, Query(max_length=50)] = None, 
        test2: Annotated[str, Query(min_length=2)] = None,
        item: Item = None #Request Body로 Pydantic 모델 형태로 받는다......
    ):
    
    rtnData = {
        "item_id": item_id,
        "test1": test1,
        "test2": test2,
        "item": item
    }
    
    return rtnData

# Path, Form
@router.post("/items_form/{item_id}")
async def update_item_form(
        
        item_id: Annotated[int, Path(..., gt=0)],
        name: Annotated[str, Form(..., min_length=2, max_length=50)],
        price: Annotated[int, Form(..., ge=0)],
        test: Annotated[Optional[str], Form(max_length=50)]=None,
        description: Annotated[Optional[str], Form(max_length=500)]=None,
        tax: Annotated[float, Form()] =None # 뒤에 = None 설정되지 않아 필수 값이 된다.
    ):
    
    rtnData = {
        "item_id": item_id,
        "test": test,
        "name": name,
        "description": description,
        "price": price,
        "tax": tax
    }    
    
    return rtnData

# Path, Query, Form을 @model_validator 적용. 
# 폼 데이터 → Item 객체로 직접 생성 (유효성 검사는 수동으로 발생)
@router.post("/items_form_01/{item_id}")
async def update_item_form_01(
        name: Annotated[str, Form(..., min_length=2, max_length=50)],
        price: Annotated[float , Form(..., ge=0)], 
        description: Annotated[str, Form( max_length=500)] = None,        
        tax: Annotated[float, Form()] = None,
    ):
    
    try: 
        item = Item(
            name=name,
            description=description,
            price=price,
            tax=tax
        )
        
        return item
    
    except ValidationError as e:
        raise RequestValidationError(e.errors())

# Item 모델 생성을 함수로 분리 → 다른 곳에서도 재사용 가능하게 함
def parse_user_form(
        name: Annotated[str, Form(..., min_length=2, max_length=50)],
        price: Annotated[float , Form(..., ge=0)], 
        description: Annotated[str, Form(max_length=500)] = None,
        tax: Annotated[float, Form()] = None,
    ) -> Item:
    
    try: 
        item = Item(
            name=name,
            description=description,
            price=price,
            tax=tax
        )
        
        return item
    
    except ValidationError as e:
        raise RequestValidationError(e.errors())     

# Form 데이터 → Item 모델 자동 생성 (Depends 사용으로 함수 실행 자동)
@router.post("/items_form_02/{item_id}")
async def update_item_form_02(
        item_id: int = Path(..., gt=0, title="The ID of the item to get"),
        q: str = Query(None, max_length=50),
        item: Item = Depends(parse_user_form)
    ):
    
    rtnData = {
        "item_id": item_id,
        "q": q,
        "item": item
    }
    
    return rtnData