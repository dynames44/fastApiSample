from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

#라우터 인스턴스
router = APIRouter(prefix="/resp", tags=["Response Exam"]  ,include_in_schema=False)

# 요청 데이터용 Pydantic 모델
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

# 응답 데이터용 Pydantic 모델
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

# JSON 응답 반환 (기본 response_class는 JSONResponse)
@router.get("/resp_json/{item_id}", status_code=status.HTTP_202_ACCEPTED)
async def response_json(item_id: int, q: str | None = None):
    return {"message": "Hello World", "item_id": item_id, "q": q},

# HTML 형식의 응답 반환
@router.get("/resp_html/{item_id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def response_html(item_id: int, item_name: str | None = None):

    html_str = f'''
    <html>
    <body>
        <h2>HTML Response</h2>
        <p>item_id: {item_id}</p>
        <p>item_name: {item_name}</p>
    </body>
    </html>
    '''
    return html_str

# GET 요청 → GET 리다이렉트
@router.get("/redirect", status_code=status.HTTP_302_FOUND)
async def redirect_only(comment: str | None = None):

    #print(f"redirect {comment}")
    url=f"/resp/resp_json/33?q={comment}"
    return RedirectResponse(url)

# POST 요청 → GET 리다이렉트
@router.post("/create_redirect")
async def create_item(
                         item_id: Annotated[int, Form()] = None
                        ,item_name: Annotated[str, Form()] = None
                      ):
    
    #print(f"item_id: {item_id} item name: {item_name}")
    url=f"/resp/resp_json/{item_id}?q={item_name}"
    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

# Pydantic 모델을 사용한 POST 요청 처리 및 응답 모델 지정
@router.post("/create_item/", response_model=ItemResp, status_code=status.HTTP_201_CREATED)
async def create_item_model(item: Item):

    # 세금 포함 가격 계산
    price_with_tax = item.price + item.tax if item.tax else item.price

    # 응답 모델에 맞춰 반환
    item_resp = ItemResp(
        name=item.name,
        description=item.description,
        price_with_tax=price_with_tax
    )
    return item_resp

# Pydantic 모델을 사용한 POST 요청 처리 및 응답 모델 지정
@router.post("/create_item_t/", response_model=ItemResp, status_code=status.HTTP_201_CREATED)
async def create_item_model(item: Item):

    # 세금 포함 가격 계산
    price_with_tax = item.price + item.tax if item.tax else item.price
    
    #하나하나 입력하기 귀찮음....객체 복사 후 
    data = item.model_dump()
    data["price_with_tax"] = price_with_tax
    item_resp = ItemResp(**data)
    
    return item_resp
