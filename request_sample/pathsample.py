from fastapi import FastAPI

# FastAPI instance 생성. 
# uvicorn 실행때 실행 파일:FastAPI 인스턴스 --port=*** --reload
#  uvicorn pathsample:app --reload
app = FastAPI(
    title="Sample Swagger UI",        
    swagger_ui_parameters={"defaultModelsExpandDepth": -1} 
) 

# Path parameter값과 특정 지정 Path가 충돌되지 않도록 uri 작성 코드 위치에 주의 
# python, Fast APi 는 인터프린터 개발 언어로 순차적 실행이 기본..(예외는 있음)
# /path/test1/all 이 /path/test1/{idx} 보다 후순위로 구현되어 있으면 param 가 정수가 아닌 문자열 이라서 오류 발생 
@app.get("/path/test1/all")
# 수행 함수 인자로 path parameter가 입력됨. 함수 인자의 타입을 지정하여 path parameter 타입 지정.  
async def all():
    return {"message": "all items"}

@app.get("/path/test1/{idx}",tags=["/Path Param Sample"], summary="Path Param Ex1", description="Path Param 예제 Type1" )
async def path1(idx : int):
    rtn = dict(message="Hello World", params=idx)
    return rtn

@app.get("/path/test2/{pathStr}",tags=["/Path Param Sample"], summary="Path Param Ex2", description="Path Param 예제 Type2" )
async def path1(pathStr : str):
    rtn = dict(message="Hello World", params=pathStr)
    return rtn