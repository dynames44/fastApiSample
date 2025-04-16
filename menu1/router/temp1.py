from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from core.templates import templates

#FastAPI 라우터 인스턴스 생성
router = APIRouter(prefix="/menu1", include_in_schema=False)  # include_in_schema:  Swagger UI 노출여부

class Item(BaseModel):
    name: str
    price: float

@router.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None): # template engine을 사용할 경우 반드시 Request 객체가 인자로 입력되어야 함. 
    
    # 내부에서 pydantic 객체 생성. 
    item = Item(name="test_item", price=10)
    
    # pydantic model값을 dict 변환. 
    item_dict = item.model_dump()
    item_dict["temp"] = "temp01"
    
    # viewData = {
    #      "request": request
    #     ,"id": id
    #     ,"q_str": q
    #     ,"item": item
    #     ,"item_dict": item_dict
    # }
    
    viewData = dict(
         request = request
        ,id = id
        ,q_str = q
        ,item = item
        ,item_dict =  item_dict        
    )

    return templates.TemplateResponse("menu1/item.html", viewData)