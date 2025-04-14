from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

# FastAPI instance 생성. 
# uvicorn 실행때 실행 파일:FastAPI 인스턴스 --port=*** --reload
app = FastAPI(
    title="Sample Swagger UI",        # Swagger UI 맨 위 제목
    swagger_ui_parameters={"defaultModelsExpandDepth": -1} # 
    #docs_url="/mydocs",          # 기존 /docs → /mydocs 로 변경
    #openapi_url="/sample.json "                # 기존 /openapi.json → /myopenapi.json 로 변경
) 

'''
    FastAPI 라우터 데코레이터
    - path: API 경로 (예: "/test")
    - methods: HTTP 메서드 (예: GET, POST 등) - ["GET", "POST"] 리스트 타입으로 들어와야 한다.
      : 메서드에 따라 @app.get(), @app.post() 등 사용
    - tags : Swagger UI 그룹  
    - summary : Swagger UI  리소스 설명      
    - description : 짧은 주석 , 긴 주석은 메소드명 아래 긴 준석 형태로 남긴다.     
'''
@app.get("/",tags=["/Sample"], summary="리소스 이름", description="주석" )
async def root():
    rtn = dict(message="Hello World")
    return rtn

@app.api_route("/test", methods=["GET", "POST"],tags=["/Sample"], summary="리소스 이름", description="주석")
async def test():
    rtn = dict(message="test")
    return rtn

#Response content-type 수정 
@app.get("/test1",tags=["/Sample"], summary="Return 변경 Type1 : text/plain", response_class=PlainTextResponse)
async def test1():
    '''
        Return content-type 수정 : 

        >  response_class 변경
    '''
    return "텍스트 응답입니다."

#Response content-type 수정 
@app.get("/test2",tags=["/Sample"], summary="Return 변경 Type2 : text/html", response_class=HTMLResponse, description="Html 타입 반환")
async def test2():
    return "<h1>Hello, HTML Response!</h1>"

@app.api_route("/search", methods=["GET"],tags=["/Sample"], summary="search", description="get param Sample")
async def search_items(
    param1: int = Query(
         default=None                   # 필수여부 (None 이면 선택값)
        ,description="숫자형 파라미터"  # Swagger UI 에 표시할 설명
        #,alias="number"                 # 요청 시 사용할 파라미터 이름
        #,deprecated=True                # 사용 중단 표시
        #,min_length=1                   # 최소 길이 (문자열일 때)
        #,max_length=10                  # 최대 길이 (문자열일 때)
        #,ge=0                           # 최소 값 (숫자일 때)
        #,le=100                          # 최대 값 (숫자일 때)        
        
    ),
    param2: str = Query(default=None    
                        ,description="문자열 파라미터")
):
    return {"param1": param1, "param2": param2}

@app.get("/path/{idx}",tags=["/Path Param Sample"], summary="Path Param Ex1", description="Path Param 예제 Type1" )
async def path1(idx : int):
    rtn = dict(message="Hello World", params=idx)
    return rtn

@app.get("/path/{pathStr}",tags=["/Path Param Sample"], summary="Path Param Ex2", description="Path Param 예제 Type2" )
async def path1(pathStr : str):
    rtn = dict(message="Hello World", params=pathStr)
    return rtn
