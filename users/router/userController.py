from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.templates import templates

#FastAPI 라우터 인스턴스 생성
router = APIRouter(prefix="/user", include_in_schema=False)

#사용자관리 메인 
@router.get("/list", response_class=HTMLResponse)
async def base(request: Request): 
    
    viewData = dict(
         request = request
            
    )

    return templates.TemplateResponse("users/list.html", viewData)