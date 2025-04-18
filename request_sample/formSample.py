from typing import Annotated
from fastapi import APIRouter, Form

#FastAPI 라우터 인스턴스 생성
router = APIRouter(prefix="/form", tags=["Request Form Exam"]  ,include_in_schema=False)

# ---------------------------
# Form 데이터를 받는 기본 예제
# ---------------------------

# Form()을 통해 HTML form 필드 데이터를 수신
# country는 선택적 (None 가능)
@router.post("/login")
async def login(
                username: str = Form(...),              # Form(...) 필수 필드
                email: str = Form(None),                # Form(None) 선택 필드
                country: Annotated[str, Form()] = None  # 선택 필드
           ):
    return {
        "username": username,
        "email": email,
        "country": country
    }

# ---------------------------
# Form(...) → 필수 필드 지정 예제
# ---------------------------

# Form(...)은 필수 입력을 명시적으로 표현
@router.post("/login_f/")
async def login(
                username: Annotated[str, Form()],              # 필수 필드
                email: Annotated[str, Form()],                 # 필수 필드
                country: Annotated[str, Form()] = None          # 선택 필드
            ):
    return {
        "username": username,
        "email": email,
        "country": country
    }

# ---------------------------
# Path, Query, Form 파라미터를 함께 사용하는 예제
# ---------------------------

@router.post("/login_pq/{login_gubun}")
async def login(
    login_gubun: int,                                   # Path Parameter
    q: str | None = None,                               # Query Parameter
    username: str = Form(),                             # Form 필드
    email: str = Form(),                                # Form 필드
    country: Annotated[str, Form()] = None              # 선택적 Form 필드
):
    return {
        "login_gubun": login_gubun,
        "q": q,
        "username": username,
        "email": email,
        "country": country
    }
