from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

#FastAPI 라우터 인스턴스 생성
router = APIRouter(prefix="/query", tags=["Request Get Query Exam"]  ,include_in_schema=False)

# 예시용 데이터베이스 역할을 하는 리스트
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 파라미터 데이터모델 :  BaseModel 정의
class paraModel(BaseModel):
    name: Optional[str] = None
    limit: Optional[int] = 10

# Query Parameter 사용 예제
# http://127.0.0.1:8000/items?skip=1&limit=1 와 같이 사용
@router.get("/items")
async def read_item(skip: int = 0, limit: int = 2): #파라미터 값이 없을때 파라미터별 default 깂 지정 가능...
     
    end : int = skip + limit
    print(f"skip:::::{skip}, limit::::::{limit},end:::::{end}")
    
    return fake_items_db[skip: end]


# 필수 Query Parameter 사용 예제
# skip과 limit에 기본값이 없으므로, 요청 시 반드시 값이 제공되어야 함
# http://127.0.0.1:8000/items_nd/?skip=1&limit=2 와 같이 사용
@router.get("/items_nd/")
async def read_item_nd(skip: int, limit: int): 
    end : int = skip + limit
    print(f"skip:::::{skip}, limit::::::{limit},end:::::{end}")
    return fake_items_db[skip: end]

# 선택적 Query Parameter 예제
# limit은 선택 사항이며 기본값은 None임
# Optional[int] 또는 int | None 형태로 타입 힌트를 줄 수 있음
# http://127.0.0.1:8000/items_op/?skip=1 와 같이 limit 없이도 호출 가능
@router.get("/items_op/")
async def read_item_op(skip: int, limit: Optional[int]= None): #Optional을 쓰더라도 = None을 생략 할수 없다...무조건 써야됨
    if limit:
        
        end : int = skip + limit
        print(f"skip:::::{skip}, limit::::::{limit},end:::::{end}")
        
        return fake_items_db[skip: end]
    else:
        return {"limit is not provided"}

# 선택적 Query Parameter 예제
# limit은 선택 사항이며 기본값은 None임
# Optional[int] 또는 int | None 형태로 타입 힌트를 줄 수 있음
# http://127.0.0.1:8000/items_op/?skip=1 와 같이 limit 없이도 호출 가능
@router.get("/items_op1/")
async def read_item_op(skip: int, limit = None): 
    if limit:
        
        end : int = skip + limit
        print(f"skip:::::{skip}, limit::::::{limit},end:::::{end}")
        
        return fake_items_db[skip: end]
    else:
        return {"limit is not provided"}

# Path Parameter와 Query Parameter 혼합 사용 예제
# item_id는 URL 경로에 포함되고, q는 선택적 쿼리 파라미터
# 예: http://127.0.0.1:8000/items/abc?q=somequery
@router.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Parameter BaseModel 사용 예제
# 파라미터 개별 시용이 아닌 BaseModel등록 후 사용(Like DTO)
# 별칭 : BaseModel  = Depends() 선언 : 필수 - get 방식으로 BaseModel 사용시 Depends() 선언을 필수로 해야 한다.
# http://127.0.0.1:8000/items_model/?name=bong&limit=2 와 같이 사용
@router.get("/items_model/")
async def item_model(params: paraModel = Depends()): 
   return {"name": params.name, "limit" : params.limit}