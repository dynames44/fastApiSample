from fastapi import FastAPI
from request_sample import bodyRouter, formRouter, objectRouter, pathRouter, queryRouter
from response_sample import resRouter

# FastAPI instance 생성. 
# uvicorn 실행때 실행 파일:FastAPI 인스턴스 --port=*** --reload
# 실행 명령어: uvicorn main:app --port=8080 --reload
app = FastAPI(
    title="FastAPI Sample Swagger UI",        # Swagger UI 맨 위 제목
    swagger_ui_parameters={"defaultModelsExpandDepth": -1} # 
    #docs_url="/mydocs",          # 기존 /docs → /mydocs 로 변경
    #openapi_url="/sample.json "                # 기존 /openapi.json → /myopenapi.json 로 변경
) 

app.include_router(bodyRouter)
app.include_router(formRouter)
app.include_router(objectRouter)
app.include_router(pathRouter)
app.include_router(queryRouter)

app.include_router(resRouter)