from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

#main.py에서 템플릿 직접 지정 할 일이 잇을때 활성화  
#from core.templates import templates

#router
from response_sample import resRouter
from request_sample import bodyRouter, formRouter, objectRouter, pathRouter, queryRouter
from menu1.router import view1
from users.router import userController


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

app.include_router(view1) #Jinja2 샘플
app.include_router(userController) #사용자 관리 

# Static 파일 mount 
# app.mount("클라이언트가 접근할 URL 경로", StaticFiles("실제 정적파일 경로"), name="템플릿에서 사용할 이름")
app.mount("/files", StaticFiles(directory="view/static"), name="assets")

