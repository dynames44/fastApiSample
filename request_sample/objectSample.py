from fastapi import FastAPI, Request

# FastAPI 애플리케이션 인스턴스 생성
# 실행: uvicorn objectSample:app --port=8080 --reload
app = FastAPI(
    title="Sample Swagger UI",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}  # Swagger에서 모델 숨기기
)

# ---------------------------
# GET 요청: Request 객체 사용 예 (쿼리 파라미터 기반)
# ---------------------------
@app.get("/objs")
async def read_item(request: Request):
    client_host = request.client.host                   # 클라이언트 IP 주소
    headers = request.headers                           # 요청 헤더 전체
    userAgent = request.headers.get("user-agent")       # 사용자 에이전트
    auth = request.headers.get("authorization")         # 인증 토큰 (Bearer, Basic 등)
    content_type = request.headers.get("content-type")  # application/json | application/x-www-form-urlencoded | multipart/form-data; boundary=...
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    query_params = request.query_params                 # 쿼리 문자열 파라미터 (?key=value)
    url = request.url                                   # 전체 요청 URL
    path_params = request.path_params                   # 경로 파라미터 (없으면 빈 dict)
    http_method = request.method                        # 요청 HTTP 메서드

    # 헤더 항목 전체 출력     
    # for k, v in request.headers.items():
    #     print(f"{k}: {v}")

    return {
        "client_host": client_host,
        "headers": headers,
        "userAgent": userAgent,
        "auth": auth,
        "content_type": content_type,
        "origin": origin,
        "referer": referer,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method": http_method
    }

# ---------------------------
# GET 요청: Path 파라미터 포함
# ---------------------------
@app.get("/objs/{item_group}")
async def read_item_p(request: Request, item_group: str):
    client_host = request.client.host
    headers = request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method": http_method
    }

# ---------------------------
# POST 요청: JSON Body 처리 - Content-Type: application/json 형태로 넘어온 Body Data를 받아온다.
# ---------------------------
@app.post("/objs_json/")
async def create_item_json(request: Request):
    data = await request.json()        # JSON 파싱 (Content-Type: application/json)
    print("received_data:", data)
    return data

# ---------------------------
# POST 요청: Form Body 처리 
# ---------------------------
@app.post("/objs_form/")
async def create_item_form(request: Request):
    data = await request.form()        # Form 파싱 (Content-Type: application/x-www-form-urlencoded or multipart/form-data)
    print("received_data:", data)
    return {"received_data": data}

# ---------------------------
# 추가 예제: 쿠키와 원시 body 데이터 읽기
# ---------------------------
@app.post("/objs_misc/")
async def read_misc_info(request: Request):
    cookies = request.cookies                          # 요청 쿠키들
    raw_body = await request.body()                    # 원시 Body 데이터 (bytes)
    content_type = request.headers.get("content-type") # Content-Type 확인

    return {
        "cookies": cookies,
        "content_type": content_type,
        "raw_body": raw_body.decode("utf-8", errors="ignore")
    }
