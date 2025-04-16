from fastapi import APIRouter, Body
from pydantic import BaseModel

#FastAPI 라우터 인스턴스 생성
router = APIRouter(prefix="/body", tags=["Request Body Exam"])

# ---------------------------
# Pydantic 모델 정의
# ---------------------------

# 요청(Request Body)을 표현하는 모델 - 아이템 정보
# 모든 필드는 JSON 입력을 바인딩하기 위해 사용
class Item(BaseModel):
    name: str                                # 필수 필드
    description: str | None = None           # 선택 필드 (None 허용)
    price: float | None = None               # 선택 필드
    tax: float | None = None                 # 선택 필드

# 사용자 정보 모델
class User(BaseModel):
    username: str                            # 필수 필드
    full_name: str | None = None             # 선택 필드

# ---------------------------
# POST: 단일 Request Body
# ---------------------------

# 클라이언트가 JSON 형태로 Item 데이터를 보낼 경우 자동으로 바인딩됨
@router.post("/items")
async def create_item(item: Item):
    print("###### item type:", type(item))  # <class 'Item'>
    print("###### item:", item)             # Pydantic 객체 출력
    return item                             # 그대로 응답

# ---------------------------
# POST: Request Body 활용한 로직 처리
# ---------------------------

@router.post("/items_tax/")
async def create_item_tax(item: Item):
    # Pydantic 객체를 dict로 변환
    # Pydantic 객체는 변경 불가능 항목 추가 등을 위해 얇은 복사 
    item_dict = item.model_dump()
    print("#### item_dict:", item_dict)

    # 세금 정보가 있을 경우 가격 계산 후 추가
    if item.tax and item.price:
        price_with_tax = item.price + item.tax
        item_dict["price_with_tax"] = price_with_tax

    return item_dict

# ---------------------------
# PUT: Path + Query + Request Body 함께 사용
# ---------------------------
@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    
    # item 모델 + 파라미터 item_id = 새로운 딕셔너리 객체 생성 
    # result = item.model_dump(); result["item_id"] = item_id 동일 
    # 그냥 예제 맛드는 놈이 허세 부린거라고 이해하면 속편함 
    result = {"item_id": item_id, **item.model_dump()}

    # 쿼리 파라미터가 존재하면 결과에 포함
    if q:
        result["q"] = q

    print("#### result:", result)
    return result

# ---------------------------
# PUT: 여러 개의 Request Body 받기
# ---------------------------
@router.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User):
    # item, user 둘 다 JSON Body에서 받아야 함
    # 요청 예시 JSON:
    # {
    #   "item": { "name": "Pen", "price": 1.5 },
    #   "user": { "username": "alice" }
    # }
    results = {
        "item_id": item_id,
        **item.model_dump(),  # 언팩
        "user": user
    }

    print("results:", results)
    return results
