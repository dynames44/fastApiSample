from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from core.templates import templates

#FastAPI 라우터 인스턴스 생성
router = APIRouter(prefix="/jinja", include_in_schema=False)  # include_in_schema:  Swagger UI 노출여부

class Item(BaseModel):
    name: str
    desc: str

@router.get("/base/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None): # template engine을 사용할 경우 반드시 Request 객체가 인자로 입력되어야 함. 
    
    # 내부에서 pydantic 객체 생성. 
    item = Item(name="jinja_base", desc="Jinja2 기본..")
    
    # pydantic model값을 dict 변환. 
    item_dict = item.model_dump()
    item_dict["url"] = "/jinja/base/"+id
    
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

    return templates.TemplateResponse("menu1/base.html", viewData)

@router.get("/if_sample")
async def read_item_by_gubun(request: Request, gubun: str):
    
    item = Item(name="if_sample", desc="If 조건문...")

    item_dict = item.model_dump()
    item_dict["url"] = "/jinja/if_sample"

    viewData = dict(
         request = request
        ,gubun = gubun
        ,item = item_dict
    )    

    return templates.TemplateResponse("menu2/if_sample.html",viewData)